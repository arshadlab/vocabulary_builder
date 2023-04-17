#!/usr/bin/python
"""
python 3.8
This script extracts NOT common words from provided source.  Intended users are 
Source can be a text file, pdf file or a URL.  Two output files are generated.
An HTML file and a plain text file.  HTML file contains word with meaning and link to more detail explaination.

Note:
excluded_word.txt include list of words to exclude.
Run 'pip install -r requirements.txt' to install dependencies

Usage: python word_extractor.py -s <file/url> -t [minimum word length] -o [output file name]

-s <file/pdf/url>
-t Minimum word length to consier (optional, default 3)
-o output filename base (optional, default result)

Examples:
   python word_extractor.py -s Meet_Joe_Black.srt 

author: <arshadm78 @ yahoo.com>
"""

import PyPDF2
import re
import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse
import nltk

nltk.download("stopwords")
# nltk.download('punkt')
nltk.download("wordnet")
nltk.download("words")
from nltk.corpus import stopwords, words
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

wnl = WordNetLemmatizer()


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def gettextfromurl(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    words = []
    # Extract words
    for text in soup.stripped_strings:
        words.extend(text.lower().split())
    return words


def gettextfrompdf(file):
    
    # Open the PDF file
    pdf_file = open(file, "rb")

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)
    words = []
    # Loop through each page and extract the text
    for page in range(num_pages):
        # Get the page object
        pdf_page = pdf_reader.pages[page]

        # Extract the text from the page
        page_text = pdf_page.extract_text().lower()

        # Split the text into words
        words += page_text.split()

    # Close the PDF file
    pdf_file.close()

    return words


def gettext(file):
    
    text_file = open(file, "r")
    text = text_file.read().lower().replace(".", "").replace("--", "")
    
    pattern = "[a-zA-Z\-\.'/]+"
    words = re.findall(pattern, text)
    
    text_file.close()
    return words


def getFinalList(text_list, min_length=3):
    wordnet_tag = ["n", "s", "a", "r", "v"]
    
    # initialize a null list
    unique_list = []
    with open("excluded_word.txt", "r") as f_object:
        common_words = f_object.read().split()
        
    stop_words = set(stopwords.words("english"))
    full_list = words.words()
    
    # traverse for all elements
    lem_tmp = []
    for x in text_list:
        lem = x

        for t in wordnet_tag:
            lem1 = wnl.lemmatize(x, t)
            # Use shortest form
            if len(lem1) < len(x):
                lem = lem1

        # check if exists in unique_list or not
        if len(lem) > min_length and lem.isalpha():
            if lem not in common_words and lem not in stop_words and lem in full_list:
                # if x != lem:
                #    final_word = x + " [" + lem + "]"
                # else:
                final_word = lem
                if final_word not in unique_list:
                    unique_list.append(final_word)

    return unique_list


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--mode",
        help="Input source type. text, pdf or url",
        required=False,
        type=str,
    )
    parser.add_argument(
        "-s", "--source", help="Input source. text, pdf or url", required=True, type=str
    )
    parser.add_argument(
        "-t", "--threshold", help="Minimum word size to consider", default=3, type=int
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file base name",
        default="result",
        required=False,
        type=str,
    )
    
    arg_list = parser.parse_args()
    
    word_lst = []
    if uri_validator(arg_list.source):
        word_lst = gettextfromurl(arg_list.source)
    elif arg_list.source.endswith(".pdf"):
        word_lst = gettextfrompdf(arg_list.source)
    else:
        word_lst = gettext(arg_list.source)

    final_list = getFinalList(word_lst, arg_list.threshold)

    # Define the initial HTML content
    html_content = "<html><head></head><body>"
    html_content += f"<h1>Source: {arg_list.source}</h1>"
  
    count = 1
    for word in final_list:
        wnl.lemmatize(word, "v")
        synsets = wn.synsets(word)
        if len(synsets) == 0:
            continue
        html_content += f"<h2>{count} - <a href='https://www.merriam-webster.com/dictionary/{word}'>{word.capitalize()}</a> </h2>"
        html_content += "<ul>"
        for synset in synsets:
            html_content += "<ul>"
            # for definition in synset.definition():
            html_content += f"<li>{synset.definition().capitalize()}</li>"
            for example in synset.examples():
                html_content += "<br>   '" + example.capitalize() + "'</br>"
            html_content += "<br></br></ul>"
        html_content += f"<a href='https://www.google.com/search?tbm=isch&q={word}'> Image search </a></ul>"
        count += 1
    html_content += "</body></html>"
    # Write the HTML content to a new file
    with open(arg_list.output + ".html", "w") as f:
        f.write(html_content)
        f.close()

    with open(arg_list.output + ".txt", "w") as f:
        f.write("\n".join(final_list))
        f.close()
        
    print(f"HTML written to {arg_list.output}.html")
    print(f"Words written to {arg_list.output}.txt")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback

        traceback.print_exc()
