class Website(object):
    url = ""
    title = ""
    description = ""
    keywords = []
    robots_index = True
    h1s = []
    links = []
    images = []
    non_html = ""
    score = 0
    pagerank = 0

    def __init__(self, url="", title="", h1s=[], links=[], images=[], non_html="",
                 description="", keywords=[], robots_index=True, pagerank=0):
        self.url = url
        self.title = title
        self.description = description
        self.keywords = keywords
        self.robots_index = robots_index
        self.h1s = h1s
        self.links = links
        self.images = images
        self.non_html = non_html
        self.pagerank = pagerank