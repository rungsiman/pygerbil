from pygerbil.examples.spotlight import Spotlight
from pygerbil.experiments.a2kb import A2KB
from pygerbil.gerbil import GerbilNIFCollection


GERBIL_ENDPOINT = 'http://gerbil.aksw.org/gerbil'
HANDLER_ENDPOINT = 'http://ec2-18-176-236-209.ap-northeast-1.compute.amazonaws.com'


def spotlight(collection: GerbilNIFCollection, text: str) -> GerbilNIFCollection:
    for phrase in Spotlight(text).phrases:
        collection.phrases.add_phrase(beginIndex=phrase.offset,
                                      endIndex=phrase.end_index,
                                      taIdentRef=phrase.uri)

    return collection

a2kb = A2KB(gerbil=GERBIL_ENDPOINT,
            handler=HANDLER_ENDPOINT,
            matching=A2KB.Matching.WEAK,
            annotators=[A2KB.Annotators.DBpedia_Spotlight,
                        spotlight],
            datasets=[A2KB.Datasets.DBpediaSpotlight])

a2kb.test()
