from pynif import NIFCollection


class GerbilNIFCollection:
    def __init__(self, context: str, mention: str):
        self.collection = NIFCollection()
        self.context = context
        self.mention = mention
        self.phrases = self.collection.add_context(self.context, self.mention)

    @property
    def turtle(self) -> str:
        return self.collection.dumps(format='turtle')


class CustomDataset:
    name: str

    def __init__(self, tag: str, fp):
        self.tag = tag
        self.fp = fp
