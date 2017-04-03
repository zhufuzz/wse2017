import urllib
def get_page(url):
    """  (string) -> string
    Accepts an url as a parameter and returns the html contents of the page.
    """
    try:
	return urllib.urlopen(url).read()
    except:
	return ""

def get_next(page):
        """  string -> tuple
        Returns the next url in the page and position of the closing quotes of the url.
        """    
        # Assigns the position of the first occurence of '<a href=' in the web-page.
        start_link = page.find('<a href=') 
        if start_link == -1:
            return None, 0	
	#  Assigns the position of the first occurence of ' after the start_link.
	# It indicates the position of the quotes before  the url.
	start_quote = page.find('"', start_link) 
	
	# Assigns the position of the next occurence of ' after start_quote.
	# It indicates the position of the quotes after  the url.
	end_quote = page.find('"', start_quote + 1)
	
	# Extract all the characters between first quote and end_quote. 
	# It contains the url.
	url = page[start_quote + 1 : end_quote] 
	 
	return url, end_quote

def get_all_links(page):  #loops through the entire page
    """ string -> list 
    Returns the list of urls present in the html contents of a web-page.
    """
    links = []
    while True: 
	url, endpos = get_next(page) 
	if url:
		links.append(url) 
		page = page[endpos:] 
	else:
		break 
    return links

union = lambda x , y: list(set(x).union(set(y)))

def crawl_web(seed):
        """ str -> list
        Returns a list of urls that can be reached by following the links 
        in seed page.
        """
	to_crawl = [seed]
	crawled = []
	index = {}
	graph = {}
	while to_crawl:
		page = to_crawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph [page] = outlinks
			union(to_crawl,outlinks)
			crawled.append(page)
	return index, graph


def add_to_index(index, key, url):
        """ (dict, string, string) -> None
        Updates the index by adding url to the list of urls associated with the keyword.
        """
	if key in index:
		index[key].append(url)
	else:
		index[key] = [url]
	
def lookup(index, key):
        """ (dict, string) -> list
        Returns the list of all urls associated with the keyword.
        """
	if key in index:
		return index[key]
	else:
		return None

def add_page_to_index(index, url, content):
        """ (list, string, string)
        Updates the index with the words present in the web-page content.
        """
	words = content.split()
	for word in words:
		add_to_index(index, word, url)

def record_user_click(index,keyword,url):
    """
    Records the links for a particular link.
    """
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] += 1

def compute_ranks(graph):
    d = 0.8
    numloops = 40

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            #Loop throught all pages
            for node in graph:
                #check if node links to page
                if page in graph[node]:
                    #Add to new rank based on this node
                    newrank += d * ranks[node] / len(graph[node])
            newranks[page] = newrank
        ranks = newranks
    return ranks
    
                                    
index, graph = crawl_web('http://xkcd.com/353')
print add_page_to_index(index, 'fake.test', "This is a test.")
for keyword in index.keys():
    print keyword, index[keyword]    
print type(index)
#print crawl_web('http://xkcd.com/353')
#print index
for i in index:
    print i, index[i]
    print