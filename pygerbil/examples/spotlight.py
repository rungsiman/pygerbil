import json
import requests
import time
from typing import Dict


SPOTLIGHT_ENDPOINT = 'https://api.dbpedia-spotlight.org/en/annotate'
SPOTLIGHT_RETRY_LIMIT = 3
SPOTLIGHT_RETRY_DURATION_SEC = 5


class SpotPhrase:
    def __init__(self, phrase: Dict[str, str]):
        self.phrase = phrase
        self.uri = phrase['@URI']
        self.support = int(phrase['@support'])
        self.types = phrase['@types'].split(',')
        self.surfaceForm = phrase['@surfaceForm']
        self.offset = int(phrase['@offset'])
        self.similarityScore = float(phrase['@similarityScore'])
        self.percentageOfSecondRank = float(phrase['@percentageOfSecondRank'])

    def __str__(self):
        return str(self.phrase)

    @property
    def end_index(self) -> int:
        return self.offset + len(self.surfaceForm)


class Spotlight:
    def __init__(self, query: str, **kwargs):
        r, t = dict(), 0

        while t < SPOTLIGHT_RETRY_LIMIT:
            try:
                r = requests.get('https://api.dbpedia-spotlight.org/en/annotate',
                                 params={'text': query, **kwargs},
                                 headers={'accept': 'application/json'}).json()
                break

            except json.decoder.JSONDecodeError:
                t += 1
                time.sleep(SPOTLIGHT_RETRY_DURATION_SEC)

        self.json = r
        self.text = r['@text']
        self.confidence = r['@confidence']
        self.support = r['@support']
        self.types = r['@types']
        self.sparql = r['@sparql']
        self.policy = r['@policy']
        self.phrases = [SpotPhrase(e) for e in r['Resources']] if 'Resources' in r else []

    def __str__(self):
        return str(self.json)
