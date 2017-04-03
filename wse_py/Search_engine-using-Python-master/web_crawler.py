import urllib
def get_page(url):
    """  (string) -> string
    Accepts an url as a parameter and returns the html contents of the page.
    """
    try:
	return urllib.urlopen(url).read()
    except:
	return ""

def get_next_link(page):
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

def print_all_links(page): 
	while True: 
		url, endpos = get_next_link(page) #calls get_next() function . It returns url and pos. Assign it to two variables.
		if url:  
		    # If it is a valid url, print it.
			print url 
			# Repeat the search from the position of last character of url.
			page = page[endpos:]
		else:
			break 

#print(print_all_links(get_page("http://en.wikipedia.org/wiki/Udacity")))
print_all_links(get_page('http://xkcd.com/353'))