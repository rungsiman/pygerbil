from . import BaseExperiment


class OKE2015Task2(BaseExperiment):
    class Matching(BaseExperiment.Matching):
        WEAK = 'WEAK_ANNOTATION_MATCH'
        STRONG = 'STRONG_ANNOTATION_MATCH'

    class Annotators(BaseExperiment.Annotators):
        Cetus = 'Cetus'
        Cetus_FOX = 'Cetus_FOX'

    class Datasets(BaseExperiment.Datasets):
        OKE_2015_Task_2_evaluation_dataset = 'OKE 2015 Task 2 evaluation dataset'
        OKE_2015_Task_2_example_set = 'OKE 2015 Task 2 example set'
        OKE_2015_Task_2_gold_standard_sample = 'OKE 2015 Task 2 gold standard sample'
        OKE_2016_Task_2_evaluation_dataset = 'OKE 2016 Task 2 evaluation dataset'
        OKE_2016_Task_2_example_set = 'OKE 2016 Task 2 example set'
        OKE_2016_Task_2_gold_standard_sample = 'OKE 2016 Task 2 gold standard sample'

    experiment = 'OKE_Task2'
