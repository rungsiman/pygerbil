import datetime
import hashlib
import json
import os
import random
import requests
import string
import threading
import time
from bs4 import BeautifulSoup
from typing import Any, Callable, Dict, List, Tuple, Union

from flask import Flask, jsonify, request, Response
from pynif import NIFCollection


HANDLER_LIFETIME_SEC = 300
WAIT_CHECK_DURATION_SEC = 0.1
WAIT_RETRIES = 100

app = Flask(__name__)
app.secret_key = bytes(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32)), encoding='utf-8')


def query_manager() -> None:
    def check_result(gerbil: str, experiment_id: str) -> Union[Dict[str, Any], None]:
        soup = BeautifulSoup(requests.get('%s/experiment' % gerbil, params={'id': experiment_id}).text, 'html.parser')

        if 'The experiment is still running' not in soup.text:
            cs, aes = list(), list()

            for itr, tr in enumerate(soup.find('table', id='resultTable').findChildren('tr')):
                if itr == 0:
                    cs = [th.text for th in tr.findChildren('th') if len(th.text)]
                    cs.insert(0, 'Status')
                    cs.insert(2, 'Task')
                    cs.append('Note')

                else:
                    tds = tr.findChildren('td')
                    ads = list()
                    note = None

                    for td in tds:
                        if 'colspan' in td.attrs:
                            note = td.text.strip()
                            [ads.append('') for _ in range(int(td.attrs['colspan']))]
                        else:
                            ads.append(td)

                    aes.append({**{cs[i + 1]: '' if isinstance(ads[i], str) else ads[i].text.strip() for i in range(len(ads))},
                                **{'Status': 'Success' if note is None else 'Failed', 'Note': note if note is not None else ''}})

            return {'header': cs, 'detail': aes}

        else:
            return None

    while True:
        global queries

        with lck:
            nq = dict()

            for hid, v in queries.items():
                if (datetime.datetime.now() - v['created']).total_seconds() < HANDLER_LIFETIME_SEC:
                    nq[hid] = v

            queries = nq

        for hid, q in queries.items():
            if q['experiment']['result'] is None and 'id' in q['experiment']:
                r = check_result(q['gerbil'], q['experiment']['id'])

                with lck:
                    q['experiment']['result'] = r

        time.sleep(1)


def _wait(checker: Callable[[], Any], duration: float = WAIT_CHECK_DURATION_SEC, retries: int = WAIT_RETRIES) -> Any:
    for _ in range(retries):
        r = checker()

        if r:
            return r

        time.sleep(duration)

    raise TimeoutError()


@app.route('/', methods=['GET'])
def status():
    with open('%s/web/index.html' % os.path.dirname(__file__), 'r') as f:
        return Response(f.read())


@app.route('/gerbil', methods=['POST'])
def gerbil_handler():
    def extract_string() -> Tuple[str, str]:
        for triple in nif.triples():
            if 'isString' in triple[1]:
                return str(triple[0]), str(triple[2])

    nif = NIFCollection.loads(request.data.decode('utf-8'))
    hid = request.args['handler_id']

    if 'annotator' not in request.args:
        with lck:
            queries[hid]['test']['context'], queries[hid]['test']['query'] = extract_string()

        a = _wait(lambda: queries[hid]['test']['answer'])

        with lck:
            queries[hid]['test']['answer'] = None

        return a

    else:
        with lck:
            an = queries[hid]['experiment']['annotators'][request.args['annotator']]
            an['context'], an['query'] = extract_string()

        a = _wait(lambda: an['answer'])

        with lck:
            an['answer'] = None

        return a


@app.route('/client/register', methods=['POST'])
def register_session():
    def generate_handler_id() -> str:
        return hashlib.sha256(bytes(request.remote_addr + str(datetime.datetime.now()), encoding='utf-8')).hexdigest()

    hid = generate_handler_id()

    while hid in queries:
        time.sleep(0.001)
        hid = generate_handler_id()

    with lck:
        queries[hid] = {'created': datetime.datetime.now(), 'experiment': {'result': None}, 'gerbil': request.form['gerbil']}

    return jsonify({'handler_id': hid})


@app.route('/client/test', methods=['POST'])
def test_start():
    def wait_for_test():
        with app.test_request_context():
            r = client.get(u, params=ps).json()

            with lck:
                queries[hid]['test']['result'] = 'pass' if r['testOk'] else r['errorMsg']

    hid = request.form['handler_id']

    try:
        with lck:
            queries[hid]['test'] = {'query': None, 'context': None, 'answer': None, 'result': None}

        u = '%s/testNifWs' % request.form['gerbil']
        ps = {'experimentType': request.form['type'],
              'url': '%s/gerbil?handler_id=%s' % (request.form['handler'], request.form['handler_id'])}

        t = threading.Thread(target=wait_for_test)
        t.start()

        try:
            q = {'query': _wait(lambda: queries[hid]['test']['query']), 'context': queries[hid]['test']['context']}

            with lck:
                queries[hid]['test']['query'] = None

            return jsonify(q)

        except TimeoutError:
            return Response(json.dumps({'detail': 'Time limit exceeded but Gerbil has not sent any query'}), status=500)

    except Exception as e:
        return Response(json.dumps({'detail': str(e)}), status=500)


@app.route('/client/test/answer', methods=['PATCH'])
def test_answer():
    hid = request.form['handler_id']

    if 'test' not in queries[hid]:
        return Response(json.dumps({'detail': 'No test has been submitted. Submit a test request then try again'}), status=400)

    with lck:
        queries[hid]['test']['answer'] = request.form['answer']

    return Response(status=200)


@app.route('/client/test/result', methods=['GET'])
def test_result():
    hid = request.args['handler_id']

    if 'test' not in queries[hid]:
        return Response(json.dumps({'detail': 'No test has been submitted. Submit a test request then try again'}), status=400)

    try:
        r = _wait(lambda: queries[hid]['test']['result'])

        with lck:
            queries[hid]['test']['result'] = None

        if r == 'pass':
            return Response(status=200)
        else:
            return Response(json.dumps({'detail': r}), status=500)

    except TimeoutError:
        return Response(json.dumps({'detail': 'Time limit exceeded but Gerbil has not sent any query'}), status=500)


@app.route('/client/execute', methods=['POST'])
def execute_start():
    hid, d = request.form['handler_id'], request.form['experiment_data']
    eid = client.get('%s/execute' % request.form['gerbil'], params={'experimentData': d}).text

    with lck:
        queries[hid]['experiment']['id'] = eid
        queries[hid]['experiment']['annotators'] = {a: {'query': None, 'context': None, 'answer': None}
                                                    for a in json.loads(request.form['py_annotators'])}

    return jsonify({'experiment_id': eid})


def _execute_pull(hid: str) -> Any:
    def wait():
        for _ in range(WAIT_RETRIES):
            for ak, av in ans.items():
                if av['query'] is not None:
                    aq = av['query']

                    with lck:
                        av['query'] = None

                    return ak, av['context'], aq

            if queries[hid]['experiment']['result'] is not None:
                er = queries[hid]['experiment']['result']

                with lck:
                    del queries[hid]

                return None, None, er

            time.sleep(WAIT_CHECK_DURATION_SEC)

        raise TimeoutError()

    ans = queries[hid]['experiment']['annotators']

    if hid not in queries:
        return Response(json.dumps({'detail': 'Handler id not found. Register an experiment then try again'}), status=404)

    try:
        qa, qc, qv = wait()

        if qa is not None:
            return jsonify({'annotator': qa, 'context': qc, 'query': qv})

        else:
            return jsonify({'result': qv})

    except TimeoutError:
        return Response(json.dumps({'detail': 'Time limit exceeded but Gerbil has not sent any query and no result has been issued'}), status=500)


@app.route('/client/execute/pull', methods=['GET'])
def execute_pull():
    return _execute_pull(request.args['handler_id'])


@app.route('/client/execute/answer', methods=['PATCH'])
def execute_answer():
    hid = request.form['handler_id']
    an = request.form['annotator']

    if hid not in queries:
        return Response(json.dumps({'detail': 'Handler id not found. Register an experiment then try again'}), status=404)

    with lck:
        queries[hid]['experiment']['annotators'][an]['answer'] = request.form['answer']

    return _execute_pull(request.form['handler_id'])


@app.route('/client/dataset/upload', methods=['POST'])
def upload_dataset():
    file = request.files['file']
    return jsonify(client.post('%s/file/upload' % request.form['gerbil'], files={file.filename: file.read()}).json())


queries = dict()
client = requests.Session()

lck = threading.Lock()
mgr = threading.Thread(target=query_manager)
mgr.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
