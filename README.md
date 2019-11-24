# PyGERBIL (Development)
[![Build Status](https://travis-ci.org/rungsiman/pygerbil.svg?branch=master)](https://travis-ci.org/rungsiman/pygerbil)  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/rungsiman/pygerbil)

PyGERBIL is a Python wrapper of [GERBIL](http://aksw.org/Projects/GERBIL.html) that offers API for experiment configuration, testing, and execution, as well as a simple GERBIL-compatible web server running on [Flask](https://www.palletsprojects.com/p/flask/). To test a newly created annotator, GERBIL requires a web server that consumes a series of texts in [NIF format](https://persistence.uni-leipzig.org/nlp2rdf/) and produces annotations, also in NIF format. PyGERBIL's lightweight web server acts as a middleware that manages communications between a GERBIL server and an annotator running locally. The local API streamlines the entire experimentation process into a few lines of code.

# Demo
![Uptime Robot status](https://img.shields.io/uptimerobot/status/m783868318-8f8eaca6a87fb7500f103a39?label=server%20status)

Visit this [Jupyter notebook](http://ec2-18-179-56-1.ap-northeast-1.compute.amazonaws.com) for an example of how to build a custom annotator and execute an experiment with PyGERBIL. You can also use the server where the notebook is located to conduct try your own experiments. However, please keep in mind that this server is for demonstration only and may be terminated at any time.

# Installation
##### Client
PyGERBIL can be installed directly from a GitHub repository using pip command:
```sh
pip install git+https://github.com/rungsiman/pygerbil
```

##### Web Server
PyGERBIL's lightweight web server can operate on machines with very limited resources such as [AWS t3a.nano](https://aws.amazon.com/ec2/instance-types/t3/). To start a server, clone this repository then navigate to PyGERBIL package location and install packages from requirements.txt. Once all dependencies are insalled, find serv.py within the package and start the Flask web server.
```sh
git clone https://github.com/rungsiman/pygerbil
pip install -r requirements.txt
env FLASK_APP=serv.py flask run
```

# Usage
The experiment templates are available in `pygerbil.experiments`. To create an experiment, first import the template, then create a class instance. For example, the following code setups, tests, and executes an `A2KB` experiment:
```python
from pygerbil.experiments.a2kb import A2KB

a2kb = A2KB(gerbil=GERBIL_ENDPOINT,
            handler=HANDLER_ENDPOINT,
            matching=A2KB.Matching.WEAK,
            annotators=ANNOTATORS,          # A list of existing or newly created annotators
            datasets=DATASETS)              # A list of existing datasets or datasets to be uploaded

if a2kb.test():
    a2kb.execute().result.beautify()
```
The `beautify()` function returns a multi-line string containing a table for display in standard output. Without it, the `result` property would return a list of dictionaries that can be exported directly in a JSON format.

PyGERBIL provides lists of annotators and datasets available on GERBIL such as `A2KB.Annotators.DBpedia_Spotlight` and `A2KB.Datasets.DBpediaSpotlight`. To test a custom annotator, create a function that takes `GerbilNIFCollection` and a string as arguments, and returns an annotated `GerbilNIFCollection`.
```python
from pygerbil.gerbil import GerbilNIFCollection

def annotator(collection: GerbilNIFCollection, text: str) -> GerbilNIFCollection:
    for phrase in phrases:
        collection.phrases.add_phrase(phrase.beginIndex, 
                                      phrase.endIndex, 
                                      phrase.taIdentRef)
    return collection
```
Refer to [pynif](https://pypi.org/project/pynif/) for how to use the `add_phrase` function. When a text is sent from GERBIL, a PyGERBIL web server forwards the text and its context to its client, which subsequently calls the `annotator` function, compiles a NIF document, then sends the document back to the web server and GERBIL respectively. 

To compare DBpedia Spotlight annotator against the created `annotator` on A2KB, set the `annotators` argument of A2KB to:
```python
a2kb = A2KB(annotators=[A2KB.Annotators.DBpedia_Spotlight, annotator])
```
PyGERBIL runs silently by default, but it provides a logging machanism. To enable logging, import Python's built-in logging module and set its configuration:
```python
import logging

logging.basicConfig(level=logging.INFO)
```
To get started, check out a quick example of how to create a custom DBpedia Spotlight annotator in this [Jupitor notebook](http://ec2-18-179-56-1.ap-northeast-1.compute.amazonaws.com)

# Development
PyGERBIL is still in its early development. It will be available on PyPi once it is more stable. All contributions are welcomed.