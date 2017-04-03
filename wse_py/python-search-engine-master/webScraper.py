import urllib2
import ssl
import string
import pageRank

ssl._create_default_https_context = ssl._create_unverified_context

def get_page_text(url,index, word_count=0):

    response = urllib2.urlopen(url)
    html = response.read()

    page_text, page_words = "", []
    html = html[html.find("<body") + 5:html.find("</body>")]

    script_start_tag = html.find("<script")
    while script_start_tag > -1:
        script_end_tag = html.find("</script>")

        # len find the length of the tag
        html = html[:script_start_tag] + html[script_end_tag + len("</script>"):]
        script_start_tag = html.find("<script")

    ignore = []
    fin = open("ignoreList.txt", "r")
    for word in fin:
        ignore.append(word.strip())
    fin.close()

    finished = False
    while not finished:
        next_close_tag = html.find(">")
        next_open_tag = html.find("<")
        if next_open_tag > -1:
            content = " ".join(html[next_close_tag + 1:next_open_tag].strip().split())
            page_text = page_text + " " + content
            html = html[next_open_tag + 1:]
        else:
            finished = True

    for word in page_text.split():
        # Setting the words to lower case and removing punctuation
        word = word.lower()
        word = word.strip(string.punctuation)

        if word[0].isalnum() and not word in ignore:
            page_words.append(word)

    for word in page_words:
        word_count += 1
        add_word_and_page_to_index(index,word, url, word_count)

def add_word_and_page_to_index(index,keyword, url, word_count):

    # index structure { 'hello' : {  'www.google.com' : [35, 24, 50] } }
    if keyword in index:
        # handle if keyword already exists
        second_dict = index[keyword]
        if url in second_dict:
            values_array = second_dict[url]
            values_array.append(word_count)
        else:
            second_dict[url] = [word_count]

    else:  # create a new dict and append to index
        second_dict = {}
        second_dict[url] = [word_count,]
        index[keyword] = second_dict

def page_scraper(graph):

    # index dictionary
    index = {}

    # looking though dictionary to find URLs.
    # Adding them to completed list once they have been scraped.
    completed_url_list = []
    for url in graph:
        if url not in completed_url_list:
            get_page_text(url,index) #get_page_Text
            completed_url_list.append(url)

    print ("\nData generated")

    rank = pageRank.compute_ranks(graph)

    return (index,rank)
