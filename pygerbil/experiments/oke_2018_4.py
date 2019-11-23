from . import BaseExperiment


class OKE2018Task4(BaseExperiment):
    class Matching(BaseExperiment.Matching):
        WEAK = 'WEAK_ANNOTATION_MATCH'
        STRONG = 'STRONG_ANNOTATION_MATCH'

    class Annotators(BaseExperiment.Annotators):
        pass

    class Datasets(BaseExperiment.Datasets):
        OKE_2018_Task_4_training_dataset = 'OKE 2018 Task 4 training dataset'

    experiment = 'OKE2018Task4'
