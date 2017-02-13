"""
using pylucene to index, query, and perform topic modeling on the wikipedia 
pages for every country in the world as well as the pages for their associated capitals
@author: msnyder
"""

## indexing

from bs4 import BeautifulSoup
import urllib
import sys
import lucene
import lda
from collections import Counter
import numpy as np
from collections import OrderedDict
from org.apache.lucene.analysis import tokenattributes
from org.apache.lucene.analysis.en import EnglishAnalyzer
from java.io import StringReader
from java.io import Reader
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import LowerCaseFilter, StopFilter, StopAnalyzer
from org.apache.pylucene.analysis import PythonAnalyzer
from org.apache.lucene.analysis.charfilter import HTMLStripCharFilter
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.index import IndexReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import Query
from org.apache.lucene.search import TopDocs
from org.apache.lucene.search import ScoreDoc
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.index import Term
from org.apache.lucene.search import TermQuery
from org.apache.lucene.search import FuzzyQuery
from org.apache.lucene.search import PhraseQuery

lucene.initVM()

def create_soup_object(url):
    raw_text = urllib.urlopen(url).read()
    main_soup = BeautifulSoup(raw_text)
    return main_soup

main_page = 'https://en.wikipedia.org/wiki/List_of_national_capitals_in_alphabetical_order'
main_soup = create_soup_object(main_page)

# 249 countries
# 11 have two capitals (montenegero has 2 capitals but 3 links in the html)
# 1 has 3 capitals
# should be 263 total links in capitals part
# should purge this down to 262 to get rid of the extra montenegro link

def create_dictionary(soup_object):
    # gets all links of countries and corresponding capitals and puts them in a dictionary where 
    # the keys are country links and the values are capitals links, values will be a list with multiple
    # links in the case that a country has more than one capital
    country_dictionary = {}
    root = 'https://en.wikipedia.org'
    country_table = soup_object.find('table', {'class':'sortable'}).find_all('tr')[1:250]
    for country in country_table:
        capitals = country.find('td').find_all('a')  
        num_capitals = len(capitals)
        countries = country.find_all('a')
        if num_capitals == 1:
            country = root+countries[1].get('href')
            capital = root+countries[0].get('href')
            country_dictionary[country] = capital
        if num_capitals == 2:
            country = root+countries[2].get('href')
            capital_1 = root+countries[0].get('href')
            capital_2 = root+countries[1].get('href')
            country_dictionary[country] = [capital_1,capital_2]
        if num_capitals == 3:
            country = root+countries[3].get('href')
            capital_1 = root+countries[0].get('href')
            capital_2 = root+countries[1].get('href')
            capital_3 = root+countries[2].get('href')
            country_dictionary[country] = [capital_1,capital_2,capital_3] 
    return country_dictionary
      
countries_dict = create_dictionary(main_soup)
# removing random third link for montenegro that didn't correspond to a capital
countries_dict['https://en.wikipedia.org/wiki/Montenegro'] = countries_dict['https://en.wikipedia.org/wiki/Montenegro'][0:2]

#print (len(countries_dict.keys())) # 249 countries ---> CHECK

def count_capitals():
    count = 0
    for key in countries_dict:
        if len(countries_dict[key]) < 5:
            count+=len(countries_dict[key])
        else:
            count+=1
    return count

#print (count_capitals()) # 262 ------> CHECK
    
def lucene_english_normalizer(text):
    # function for normalizing text scraped from wikipedia
    reader = StringReader(text)
    filter = HTMLStripCharFilter(reader)
    normalizer = EnglishAnalyzer(Version.LUCENE_4_10_1)
    english_normalizer = normalizer.tokenStream('field',filter)
    english_normalizer.reset()
    lemmas = []
    while(english_normalizer.incrementToken()):
        token = english_normalizer.getAttribute(tokenattributes.CharTermAttribute.class_).toString()
        lemmas.append(token)
    return(lemmas)

def merge_country_city_text(dictionary_object):
    # formating country and city urls and associated text into an object we can send to the index 
    all_text = []
    for country in countries_dict:
        country_capital_pair = []
        country_capital_pair.append(country)
        country_capital_pair.append(str(create_soup_object(country).find_all('p')))
        if len(countries_dict[country]) > 5:
            country_capital_pair.append(countries_dict[country])
            country_capital_pair.append(str(create_soup_object(countries_dict[country])))
            all_text.append(country_capital_pair)
        else:
            for capital in countries_dict[country]:
                country_capital_pair.append(capital)
                country_capital_pair.append(str(create_soup_object(capital)))
                all_text.append(country_capital_pair)
    return all_text

def clean_html(text):
    # cleaning the html from the text scraped from wikipedia
    english_analyzed = lucene_english_normalizer(text)
    html_clean = ''
    for token in english_analyzed:
        html_clean = html_clean + ' ' + token.encode('ascii', 'ignore')
    return html_clean

def clean_countries_dict(dictionary_object):
    cleaned = []
    for country in dictionary_object:
        country_cleaned = [country[0],clean_html(country[1]),country[2],clean_html(country[3])]
        cleaned.append(country_cleaned)
    return cleaned

cleaned_dictionary = clean_countries_dict(merge_country_city_text(countries_dict))

# creating the index
index_path = File(sys.argv[1])
analyzer = EnglishAnalyzer(Version.LUCENE_CURRENT)
index = SimpleFSDirectory(index_path)

# populating the index
config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
writer = IndexWriter(index, config)

def create_index():
    for country in cleaned_dictionary:
        doc = Document()
        doc.add(Field("country", country[0], Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("country_html", country[1], Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("capital", country[2], Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("capital_html", country[3], Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)

create_index()

#writer.deleteAll()
writer.close()
index.close()

### retrieval

index = SimpleFSDirectory(File(sys.argv[1]))
reader = IndexReader.open(index)
n_docs = reader.numDocs()
print("Index contains %d documents." % n_docs)

def get_query_results(reader,query,n,field):
    searcher = IndexSearcher(reader)
    hits = searcher.search(query, n).scoreDocs
    print("Found %d hits:" % len(hits))
    for i, hit in enumerate(hits):
        doc = searcher.doc(hit.doc)
        print("%d. %s" % (i + 1, doc.get(field)))

#### part(a)
query1a = TermQuery(Term("capital_html","greek"))
query2a = TermQuery(Term("capital_html","roman"))
query3a = TermQuery(Term("capital_html","persian"))

boolean_query_a = BooleanQuery()
boolean_query_a.add(query1a, BooleanClause.Occur.MUST)
boolean_query_a.add(query2a, BooleanClause.Occur.MUST)
boolean_query_a.add(query3a, BooleanClause.Occur.MUST_NOT)

get_query_results(reader,boolean_query_a,n_docs,"capital")

#Found 32 hits:
#1. https://en.wikipedia.org/wiki/Sukhumi
#2. https://en.wikipedia.org/wiki/Nicosia
#3. https://en.wikipedia.org/wiki/Nicosia
#4. https://en.wikipedia.org/wiki/Tiraspol
#5. https://en.wikipedia.org/wiki/Tripoli
#6. https://en.wikipedia.org/wiki/Tunis
#7. https://en.wikipedia.org/wiki/Lisbon
#8. https://en.wikipedia.org/wiki/Podgorica
#9. https://en.wikipedia.org/wiki/Cetinji
#10. https://en.wikipedia.org/wiki/Sofia
#11. https://en.wikipedia.org/wiki/Bucharest
#12. https://en.wikipedia.org/wiki/Cairo
#13. https://en.wikipedia.org/wiki/Budapest
#14. https://en.wikipedia.org/wiki/Skopje
#15. https://en.wikipedia.org/wiki/Bangui
#16. https://en.wikipedia.org/wiki/Ljubljana
#17. https://en.wikipedia.org/wiki/Zagreb
#18. https://en.wikipedia.org/wiki/Algiers
#19. https://en.wikipedia.org/wiki/Bern
#20. https://en.wikipedia.org/wiki/Dublin
#21. https://en.wikipedia.org/wiki/Montevideo
#22. https://en.wikipedia.org/wiki/Gibraltar
#23. https://en.wikipedia.org/wiki/Bratislava
#24. https://en.wikipedia.org/wiki/Berlin
#25. https://en.wikipedia.org/wiki/Madrid
#26. https://en.wikipedia.org/wiki/Kiev
#27. https://en.wikipedia.org/wiki/Amsterdam
#28. https://en.wikipedia.org/wiki/Warsaw
#29. https://en.wikipedia.org/wiki/Wellington
#30. https://en.wikipedia.org/wiki/Copenhagen
#31. https://en.wikipedia.org/wiki/Buenos_Aires
#32. https://en.wikipedia.org/wiki/Havana

#### part(b)

query1b = Term("capital_html","shakespeare")

fuzzy_query_b = FuzzyQuery(query1b)

get_query_results(reader,fuzzy_query_b,n_docs,"capital")

#Results:
#Found 4 hits:
#1. https://en.wikipedia.org/wiki/London
#2. https://en.wikipedia.org/wiki/Prague
#3. https://en.wikipedia.org/wiki/Cairo
#4. https://en.wikipedia.org/wiki/Washington,_D.C.

#### part(c)

phrase_c = PhraseQuery()
phrase_c.setSlop(10)

term_phrase_c = 'located below sea level'
token_phrase_c = lucene_english_normalizer(term_phrase_c)

def get_phrase(token_phrase):
    for word in token_phrase:
        term = Term('capital_html', word.encode('ascii', 'ignore'))
        phrase_c.add(term)

get_phrase(token_phrase_c)
get_query_results(reader,phrase_c,n_docs,'capital')

#Found 1 hits:
#Results:
#1. https://en.wikipedia.org/wiki/Baku

#### part(d)
phrase_d = PhraseQuery()
phrase_d.setSlop(10)

term_phrase_d = 'arctic circle'
token_phrase_d = lucene_english_normalizer(term_phrase_d)

def get_phrase(token_phrase):
    for word in token_phrase:
        term = Term('capital_html', word.encode('ascii', 'ignore'))
        phrase_d.add(term)

get_phrase(token_phrase_d)
get_query_results(reader,phrase_d,n_docs,'capital')

#Found 1 hits:
#1. https://en.wikipedia.org/wiki/Nuuk

### latent dirichlet allocation

# removing duplicate countries
country_text = [country[1].split() for country in cleaned_dictionary]
country_f_set = set(frozenset(country) for country in country_text)
country_text = [list(country) for country in country_f_set]

#print len(country_text) # 249 countries

country_text_counter = [Counter(country) for country in country_text]

def get_country_term_frequency(counter_object):
    dictionary = {key:value for key,value in counter_object.items()}
    return dictionary
    
country_term_frequency_dictionary = [get_country_term_frequency(counter) for counter in country_text_counter]
all_country_words = sorted(list(set([key for country_freq in country_term_frequency_dictionary for key in country_freq])))

def valid_word(word):
    is_valid = not (any(letter.isdigit() for letter in word))
    return is_valid

all_country_words_cleaned = [word for word in all_country_words if valid_word(word)]

#print len(all_country_words_cleaned) # 51071 total words

def create_country_tf_vector(country):
    vector = {key:0 for key in all_country_words_cleaned}
    for word in country:
        if word in vector:
            vector[word] = country[word]
    vector = OrderedDict(sorted(vector.items()))
    tf_country_vector = [value for value in vector.values()]
    return np.array(tf_country_vector)

country_term_freq_vector = [create_country_tf_vector(country) for country in country_term_frequency_dictionary]
country_matrix = np.array(country_term_freq_vector)

#print country_matrix.shape # 51071x249

country_model = lda.LDA(n_topics=10, n_iter=250, random_state=1)
country_model.fit(country_matrix)  
topic_word = country_model.topic_word_  
n_top_words = 10

def get_topics(input):
    for i, topic_dist in enumerate(input):
        topic_words = np.array(all_country_words_cleaned)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    
get_topics(topic_word)

#Topic 0: spanish de american u. spain puerto america countri it presid
#Topic 1: island from british french new were territori saint which zealand
#Topic 2: ha state world most which it includ on from nation
#Topic 3: africa african south countri presid french guinea sudan which coloni
#Topic 4: german countri germani sweden european europ were iceland denmark norwai
#Topic 5: arab al israel palestinian islam egypt saudi from countri were
#Topic 6: from govern were countri nation elect year popul new had
#Topic 7: china ha countri india chines sri it from malaysia asia
#Topic 8: georgia greek georgian republ turkish kosovo cypru were serbia territori
#Topic 9: russian soviet russia korea poland ukrain countri union republ armenian

