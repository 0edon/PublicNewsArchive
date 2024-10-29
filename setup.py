from codecs import open
from os.path import join, abspath, dirname
from setuptools import setup, find_packages
import os

here = abspath(dirname(__file__))

with open(join(here, 'README.md'), encoding='utf-8') as buff:
    long_description = buff.read()

setup(
    name="PublicNewsArchive",
    version="1.0",
    description="A module that allows you to get and analyze news in detail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diogocorreia01/PublicNewsArchive.git",
    author="Diogo Correia"
           "Ricardo Campos",
    author_email="diogo.correia01@outlook.com",
    packages=find_packages(),
    license='LGPLv3',
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'date-guesser-rc @ git+https://github.com/rncampos/date_guesser',
        'geopy',
        'gmplot',
        'matplotlib',
        'numpy',
        'pandas',
        'pt-core-news-lg @ https://github.com/explosion/spacy-models/releases/download/pt_core_news_lg-3.8.0/pt_core_news_lg-3.8.0-py3-none-any.whl',
        'requests',
        'spacy',
        'urllib3',
        'wordcloud',
        'yake @ git+https://github.com/LIAAD/yake'
    ]
)
