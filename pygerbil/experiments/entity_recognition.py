from . import BaseExperiment


class EntityRecognition(BaseExperiment):
    class Matching(BaseExperiment.Matching):
        WEAK = 'WEAK_ANNOTATION_MATCH'
        STRONG = 'STRONG_ANNOTATION_MATCH'

    class Annotators(BaseExperiment.Annotators):
        AIDA = 'AIDA'
        Babelfy = 'Babelfy'
        DBpedia_Spotlight = 'DBpedia Spotlight'
        Dexter = 'Dexter'
        FOX = 'FOX'
        FRED = 'FRED'
        FREME_NER = 'FREME NER'
        OpenTapioca = 'OpenTapioca'
        WAT = 'WAT'
        xLisa_NER = 'xLisa-NER'
        xLisa_NGRAM = 'xLisa_NGRAM'

    class Datasets(BaseExperiment.Datasets):
        ACE2004 = 'ACE2004'
        DBpediaSpotlight = 'DBpediaSpotlight'
        Derczynski = 'Derczynski'
        ERD2014 = 'ERD2014'
        GERDAQ_Dev = 'GERDAQ-Dev'
        GERDAQ_Test = 'GERDAQ-Test'
        GERDAQ_TrainingA = 'GERDAQ-TrainingA'
        GERDAQ_TrainingB = 'GERDAQ-TrainingB'
        IITB = 'IITB'
        KORE50 = 'KORE50'
        MSNBC = 'MSNBC'
        N3_RSS_500 = 'N3-RSS-500'
        N3_Reuters_128 = 'N3-Reuters-128'
        OKE_2015_Task_1_evaluation_dataset = 'OKE 2015 Task 1 evaluation dataset'
        OKE_2015_Task_1_example_set = 'OKE 2015 Task 1 example set'
        OKE_2015_Task_1_gold_standard_sample = 'OKE 2015 Task 1 gold standard sample'
        OKE_2016_Task_1_evaluation_dataset = 'OKE 2016 Task 1 evaluation dataset'
        OKE_2016_Task_1_example_set = 'OKE 2016 Task 1 example set'
        OKE_2016_Task_1_gold_standard_sample = 'OKE 2016 Task 1 gold standard sample'
        OKE_2017_Task_1_dataset = 'OKE 2017 Task 1 dataset'
        OKE_2017_Task_2_dataset = 'OKE 2017 Task 2 dataset'
        OKE_2017_Task_3_dataset = 'OKE 2017 Task 3 dataset'
        OKE_2018_Task_1_training_dataset = 'OKE 2018 Task 1 training dataset'
        OKE_2018_Task_2_training_dataset = 'OKE 2018 Task 2 training dataset'
        OKE_2018_Task_4_training_dataset = 'OKE 2018 Task 4 training dataset'
        Ritter = 'Ritter'
        Senseval_2 = 'Senseval 2'
        Senseval_3 = 'Senseval 3'
        UMBC_Test = 'UMBC-Test'
        UMBC_Train = 'UMBC-Train'

    experiment = 'ERec'
