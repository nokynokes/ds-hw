from collections import Counter
from zipfile import ZipFile
import zipfile
import re


kWORDS = re.compile("[a-z]{4,}")

def text_from_zipfile(zip_file):
    """
    Given a zip file, yield an iterator over the text in each file in the
    zip file.
    """
    # Open the zip file
    with zipfile.ZipFile(zip_file, "r") as zip:
        # iterate through the files
        for filename in zip.namelist():
            #print(filename)
            # open the files inside the zip
            with zip.open(filename) as f:
                # interate thru the lines
                for line in f:
                    # convert the lines from bytes to string (utf-8 encoding), then yield as an iterator 
                    # Anticipating a UnicodeDecodeError
                    yield str(line,"utf-8",errors='ignore')

def words(text):
    """
    Return all words in a string, where a word is four or more contiguous
    characters in the range a-z or A-Z.  The resulting words should be
    lower case.
    """
    lst = list(kWORDS.findall(text.lower()))
    if lst:
        return lst
    else:
        return []

def accumulate_counts(words, total=Counter()):
    """
    Take an iterator over words, add the sum to the total, and return the
    total.

    @words An iterable object that contains the words in a document
    @total The total counter we should add the counts to
    """
    assert isinstance(total, Counter)
    # dictionary = dict(total.up)
    # print(dictionary)
    # for key in dictionary:

    total.update(words)
    # Modify this function 
    #print(total)   
    return total

if __name__ == "__main__":
    # You should not need to modify this part of the code
    total = Counter()
    for tt in text_from_zipfile("../data/state_union.zip"):
        total = accumulate_counts(words(tt), total)

    for ii, cc in total.most_common(100):
        print("%s\t%i" % (ii, cc))
