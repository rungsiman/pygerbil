from . import BaseExperiment


class RT2KB(BaseExperiment):
    class Matching(BaseExperiment.Matching):
        WEAK = 'WEAK_ANNOTATION_MATCH'
        STRONG = 'STRONG_ANNOTATION_MATCH'

    class Annotators(BaseExperiment.Annotators):
        DBpedia_Spotlight = 'DBpedia Spotlight'
        FOX = 'FOX'
        FRED = 'FRED'
        FREME_NER = 'FREME NER'

    class Datasets(BaseExperiment.Datasets):
        OKE_2015_Task_1_evaluation_dataset = 'OKE 2015 Task 1 evaluation dataset'
        OKE_2015_Task_1_example_set = 'OKE 2015 Task 1 example set'
        OKE_2015_Task_1_gold_standard_sample = 'OKE 2015 Task 1 gold standard sample'
        OKE_2016_Task_1_evaluation_dataset = 'OKE 2016 Task 1 evaluation dataset'
        OKE_2016_Task_1_example_set = 'OKE 2016 Task 1 example set'
        OKE_2016_Task_1_gold_standard_sample = 'OKE 2016 Task 1 gold standard sample'
        OKE_2017_Task_3_dataset = 'OKE 2017 Task 3 dataset'
        Ritter = 'Ritter'
        UMBC_Test = 'UMBC-Test'
        UMBC_Train = 'UMBC-Train'

    experiment = 'RT2KB'
