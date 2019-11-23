from . import BaseExperiment


class RE(BaseExperiment):
    class Matching(BaseExperiment.Matching):
        STRONG = 'STRONG_ENTITY_MATCH'

    class Annotators(BaseExperiment.Annotators):
        FOX = 'FOX'

    class Datasets(BaseExperiment.Datasets):
        OKE_2018_Task_3_training_dataset = 'OKE 2018 Task 3 training dataset'
        OKE_2018_Task_4_training_dataset = 'OKE 2018 Task 4 training dataset'

    experiment = 'RE'
