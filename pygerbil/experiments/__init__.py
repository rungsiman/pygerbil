import logging
import json
from enum import Enum
from typing import Any, Callable, Dict, List, Union

import requests
from tabulate import tabulate

from pygerbil.gerbil import GerbilNIFCollection, CustomDataset


class BaseExperiment:
    class Matching(Enum):
        pass

    class Annotators(Enum):
        pass

    class Datasets(Enum):
        pass

    class Result:
        def __init__(self, header: List[str], detail: List[Dict[str, Any]]):
            self.header = header
            self.detail = detail

        def beautify(self, table_format='psql'):
            table = list()

            for e in self.detail:
                table.append([str(e[self.header[i]]) if self.header[i] in e else '' for i in range(len(self.header))])

            return tabulate(table, headers=self.header, tablefmt=table_format)

    experiment: str
    experimentId: str
    settings: Dict[str, Any]
    customDatasets: List[CustomDataset]
    result: Result

    def __init__(self, *, gerbil: str, handler: str,
                 annotators: List[Union[Annotators, Callable[[GerbilNIFCollection, str], GerbilNIFCollection]]],
                 datasets: List[Union[CustomDataset, Datasets]], matching: Matching):

        self.gerbil = gerbil.strip('/')
        self.handler = handler.strip('/')
        self.matching = matching
        self.annotators = annotators
        self.datasets = datasets
        self.handlerId = requests.post('%s/client/register' % self.handler,
                                       data={'gerbil': self.gerbil}).json()['handler_id']

        logging.info('Registered experiment handler with ID: ' + self.handlerId)

    def compile(self):
        def compile_annotators() -> List[str]:
            l = list()

            for a in self.annotators:
                if isinstance(a, self.Annotators):
                    l.append(a.value)
                else:
                    l.append('NIFWS_%s(%s/gerbil?handler_id=%s&annotator=%s)' % (a.__name__, self.handler, self.handlerId, a.__name__))

            return l

        def compile_datasets() -> List[str]:
            l = list()

            for d in self.datasets:
                if isinstance(d, self.Datasets):
                    l.append(d.value)
                else:
                    d.name = requests.post('%s/client/dataset/upload' % self.handler,
                                           files={'file': d.fp},
                                           data={'gerbil': self.gerbil,
                                                 'handler_id': self.handlerId}).json()['files'][0]['name']
                    l.append(('NIFDS_%s(%s)' % (d.tag, d.name)))

            return l

        def compile_settings() -> None:
            self.settings = {'type': self.experiment,
                             'matching': self.matching.value,
                             'annotator': compile_annotators(),
                             'dataset': compile_datasets()}

        compile_settings()
        return self

    def test(self) -> bool:
        logging.info('Initializing test')
        self.compile()

        for f in self.annotators:
            if not isinstance(f, self.Annotators):
                t = requests.post('%s/client/test' % self.handler,
                                  data={'gerbil': self.gerbil,
                                        'handler': self.handler,
                                        'type': self.experiment,
                                        'handler_id': self.handlerId})

                if t.status_code == 200:
                    tj = t.json()
                    a = requests.patch('%s/client/test/answer' % self.handler,
                                       data={'handler_id': self.handlerId,
                                             'answer': f(GerbilNIFCollection(tj['context'], tj['query']), tj['query']).turtle})

                    if a.status_code == 200:
                        r = requests.get('%s/client/test/result' % self.handler,
                                         params={'handler_id': self.handlerId})

                        if r.status_code == 200:
                            logging.info('Test passed')
                            return True
                        else:
                            raise Exception('Server error: %s' % r.json()['detail'])
                    else:
                        raise Exception('Server error: %s' % a.json()['detail'])
                else:
                    raise Exception('Server error: %s' % t.json()['detail'])

    def execute(self):
        logging.info('Executing experiment')
        self.compile()

        e = requests.post('%s/client/execute' % self.handler,
                          data={'gerbil': self.gerbil,
                                'handler_id': self.handlerId,
                                'py_annotators': json.dumps([f.__name__ for f in self.annotators if not isinstance(f, self.Annotators)]),
                                'experiment_data': json.dumps(self.settings)}).json()

        self.experimentId = e['experiment_id']
        logging.info('Experiment started with ID: ' + self.experimentId)

        p = requests.get('%s/client/execute/pull' % self.handler,
                         params={'handler_id': self.handlerId})

        if p.status_code == 200:
            pj = p.json()

            while 'result' not in pj:
                for f in self.annotators:
                    if not isinstance(f, self.Annotators):
                        if f.__name__ == pj['annotator']:
                            logging.info('Processing [' + pj['annotator'] + ']: ' + pj['query'])

                            a = requests.patch('%s/client/execute/answer' % self.handler,
                                               data={'handler_id': self.handlerId,
                                                     'annotator': pj['annotator'],
                                                     'answer': f(GerbilNIFCollection(pj['context'], pj['query']), pj['query']).turtle})

                            if a.status_code == 200:
                                pj = a.json()
                            else:
                                raise Exception('Server error: %s' % a.json()['detail'])

            logging.info('Experiment finished')
            self.result = self.Result(pj['result']['header'], pj['result']['detail'])
            return self

        else:
            raise Exception('Server error: %s' % p.json()['detail'])
