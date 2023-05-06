Word Extractor for Vocabulary Building
======================================

Non native English speakers often want a tool to auto extract non common words from a text for later reference and practice. Here I am going to share a python app to build vocabulary list out of given text. The source input could be a plain text file, pdf or a URL. The end result is a HTML file with less daily use common words extracted from source text (along with their meanings).

**Usage scenario:**

*   Extract words from a subtitle text file using the app before watching movie. Studying those words before viewing movie could greatly enhance comprehension and helps to increase vocabulary faster.
*   Use app to build word list from a technical paper/pdf.
*   Prepare a list of non common words used in a website (e.g news, articles)



The app relies on NLTK library to find word stem, lemmatization and meaning. NLTK stands for Natural Language Toolkit, it is a popular open-source Python library that provides tools and resources for working with human language data. The library offers a range of functionalities such as tokenization, stemming, lemmatization, parsing, and more.

NLTK has been widely used in many research fields, including computational linguistics, machine learning, and artificial intelligence. It also includes datasets, such as the Brown Corpus, the Gutenberg Corpus, and the WordNet lexical database.

With NLTK, developers can build programs that can understand and generate human language text, and analyze large amounts of text data. It is an essential tool for anyone working with natural language processing, sentiment analysis, and other related fields.

In this app, we are using NLTK only for lemmatization and to get word meaning using WordNet.



**Setup and Usage**
===================

**Pre-requisite**

**Dependency:** Python (Tested with version 3.8)

**Supported OS :** Linux, Windows, Mac\*

Clone repository

$ git clone https://github.com/arshadlab/vocabulary\_builder.git  
$ cd vocabulary\_builder

Install dependencies

$ pip install -r requirements.txt

**Run app**

$ python3 ./word\_extractor.py  --help  
usage: word\_extractor.py \[-h\] -s SOURCE \[-t THRESHOLD\] \[-o OUTPUT\]  
  
optional arguments:  
  -h, --help            show this help message and exit  
  -s SOURCE, --source SOURCE  
                        Input source. text, pdf or url  
  -t THRESHOLD, --threshold THRESHOLD  
                        Minimum word size to consider  
  -o OUTPUT, --output OUTPUT    
                        Output files base name

Example runs:

$ python3 ./word\_extractor.py  -s meet\_joe\_black.srt -o meet\_joe\_black  
$ python3 ./word\_extractor.py  -s paper.pdf -o paper  
$ python3 ./word\_extractor.py  -s "URL" -o url

Extract word list from all srt files in a directory
$ find <dir>/*.srt | xargs -i{} ./word_extractor.py -s {} -o $(basename -s .srt {})

Outputs:
HTML and text files are created

The text output beside html file is for convenience to add words to excluded\_words.txt as vocabulary increases. A beginner can start with default list and as he/she improves, can keep adding words to exclusion list. Words in excluded\_words.txt are not considered in generating output.

An effective way of using this app would be to generate list of words in advance and study them before watching a movie, reading a research paper or going through websites. This could greatly enhance idea comprehension and could help to rapidly increase vocabulary.

Link: https://medium.com/@arshad.mehmood/word-extractor-for-vocabulary-building-11179305561
