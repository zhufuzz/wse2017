import urllib2
import ssl
import webScraper

ssl._create_default_https_context = ssl._create_unverified_context


# Generation of Graph file for use in page rank and index
def get_url_to_crawl():
    # https://dunluce.infc.ulst.ac.uk/d12mckz/COM506/B3/test_index.html
    # prompting the user a URL which will then be crawled
    while True:
        url_to_crawl = raw_input("\nPlease enter a URL to crawl >>")

        # Removing white space
        url_to_crawl = url_to_crawl.strip(" ")

        if url_to_crawl[:7] == "http://" or url_to_crawl[:8] == "https://":
            if url_to_crawl[-1] == "/":
                url_to_crawl = url_to_crawl[:-1]
            break
        else:
            print("\nIncorrect URL entered\n")

    return [(url_to_crawl, 0)]


def get_max_depth():
    while True:
        try:
            max_depth = int(raw_input('\nPlease enter a Max to crawl within the range of 0-10 >>'))
        except ValueError:
            print 'That\'s not a number!'
        else:
            if 0 <= max_depth < 11:  # checking if it is within range
                break
            else:
                print 'Out of range. Try again'

    return max_depth


def get_all_new_links_on_page(page, prev_links):
    response = urllib2.urlopen(page)
    html = response.read()

    links, links_found_on_page, pos, all_found = [], [], 0, False
    while not all_found:
        aTag = html.find("<a href=", pos)
        if aTag > -1:
            href = html.find('"', aTag + 1)
            end_href = html.find('"', href + 1)
            url = html[href + 1:end_href]
            if url[:7] == "http://" or url[:8] == "https://":
                if url[-1] == "/":
                    url = url[:-1]
                if not url in links and not url in prev_links:
                    links.append(url)

                if url not in links_found_on_page:
                    links_found_on_page.append(url)
            close_tag = html.find("</a>", aTag)
            pos = close_tag + 1
        else:
            all_found = True
    return (links, links_found_on_page)


def crawler():
    graph = {}

    to_crawl = get_url_to_crawl()

    # list of URLs which have already been crawled
    crawled = []

    # Get max depth from user
    MAX_DEPTH = get_max_depth()

    while len(to_crawl) > 0:
        top = to_crawl.pop()
        url = top[0]
        level = top[1]

        crawled.append(url)

        # Getting links found on page ane
        new_links, links_found_on_page = get_all_new_links_on_page(url, crawled)

        # Checking the level which the URL was found at is less than the max depth
        if (level < MAX_DEPTH):
            for new_link in new_links:
                to_crawl.append((new_link, level + 1))

        # Adding in the list of links found at a particular URL
        graph[url] = links_found_on_page

    # printing urls found
    print ("\nUrls found: ")
    for url in graph:
        print url

    index, ranks = webScraper.page_scraper(graph)

    return (index, ranks, graph)
