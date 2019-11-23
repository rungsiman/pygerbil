import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="pygerbil",
    version="0.0.1",
    author="Rungsiman Nararatwong",
    author_email="rungsiman@me.com",
    description="A Python wrapper of GERBIL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    url="https://github.com/rungsiman/pygerbil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
