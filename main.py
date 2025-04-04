import re
import csv
import requests
from bs4 import BeautifulSoup

OUTPUT_CSV = "ANKIDECKbsl.csv"
INPUT_CSV = 'inputwords.csv'
csv_cleared_at_start = True



        ############################################

'''
This section takes the input csv file and makes it into a list that can be used by the output section
'''

def convertCsvToList(text_file):
    """
    Converts a simple text file to a list.
    """
    try:
        word_list = []
        with open(text_file) as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                tags = [x for x in row[1:] if x] #removes blank spaces from tags
                headword = row[0]
                word_list.append([headword,tags])

        return word_list

    except FileNotFoundError: print(f"Error: File not found at {text_file}")
    except Exception as e: print(f"An error occurred: {e}")
    
    return []

    
def arrangeOrder(word): 
    '''
    word is a list, where the second item (word[1]) contains another list of all the tags
    word[1][0], contains the frequency/order tag, like '1_essential', or '3_freq'
    word[1][0][0] contains the first part of the string, which will be 1, 2, 3, or 4
    '''
    try: 
        rank = word[1][0][0]
        rank = int(rank)
    except: rank = 10 #ranks all unknown as 10 the bottom of the list
    return rank
        
        ############################################


'''
This section clears and adds to the CSV file, nothing crazy going on
'''

def clearCsv(filename = OUTPUT_CSV):
    with open(filename, "w") as file:
        file.write('')

def addToCsv(string, filename = OUTPUT_CSV ):
    with open(filename, "a") as file:
        file.write(string + '\n')


        ############################################

'''
This section takes the list from the input section, and creates a list of Note Objects to add to the output file
'''

class Note:
    def __init__(self, *args):
        args = args[0]
        self.headword = args[0]
        self.definition = args[1]
        self.example = args[2]
        self.video_url = args[3]
        self.video_title = args[4]
        self.url = args[5]
        self.tags = [normalize_tag(x) for x in args[6]]
        self.showcase = f"{self.headword}- vid:{self.video_title}, tags: {" ".join(self.tags)}"

    def __str__(self): 
    #this is a string in csv format so it can be written to the output csv file
        tag_str = " ".join(self.tags)

        joined = ";".join(
            [
                normalize_csv(self.headword),
                normalize_csv(self.definition),
                normalize_csv(self.example),
                f"[sound:{self.video_url}]",
                normalize_csv(self.video_url),
                normalize_csv(self.video_title),
                normalize_csv(self.url),
                normalize_csv(tag_str),
            ]
        )

        return joined

def normalize_tag(string):
    return string.replace(" ", "_")

def normalize_csv(string):
    doubled_quotes = string.replace('"', '""')
    return f'"{doubled_quotes}"'




def get_page(url):
    html = requests.get(url).text
    page = BeautifulSoup(html, "lxml")
    return page


def get_definitions(w, tags):
    url = 'https://www.signbsl.com/sign/'+w
    page = get_page(url)

    notes = []
    headings = [page.find("h1")] + page.find_all("h2")

    if not page.find_all(itemprop="video"):
        notes.append(Note([w, 'TRANSLATION NOT FOUND', '', '', '', '', tags+['NOTFOUND'] ]))
        print('--'+w+': TRANSLATION NOT FOUND')
        return notes

    for heading in headings:
        headword = heading.text
        tags += [x.text for x in heading.find_next_siblings("span")]
        first_p = heading.find_next_sibling("p")
        def_string = re.findall("</b> (.*?)<br/>", str(first_p))
        if def_string:
            definition = def_string[0]
        else:
            definition = ""
        italics = first_p.find("i")
        if italics is not None:
            example = italics.text
        else:
            example = ""
        video_div = first_p.find_next(itemprop="video")
        video_url = video_div.find(itemprop="contentURL")["content"]
        video_title =  w
        note_to_add = Note([headword, definition, example, video_url, video_title, url, tags])
        notes.append( note_to_add )
        
        return notes



def getCardsFromWords(w_list):
    '''
    adds each word (which may have multiple cards) to output csv
    '''
    notes_list = []
    for w in w_list:
        print( w[0]+': Contacting page...')
        notes = get_definitions(w[0], w[1]) 
        #notes returns as list, since you can have more than one note per word
        
        for note in notes:  
            print( note.headword+': Adding to '+OUTPUT_CSV+'...')
            addToCsv( str(note) ) #adds all new words to output csv

        notes_list += notes
    return notes_list #this isn't actually used, but has been kept for testing

        ############################################



if __name__ == "__main__":

    if csv_cleared_at_start: clearCsv()

    word_list = convertCsvToList(INPUT_CSV)
    word_list.sort( key=lambda word_list: arrangeOrder(word_list))
    getCardsFromWords(word_list)