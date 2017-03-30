#encoding=utf-8
from datetime import datetime

from SearchEngine.crawler import CourseCrawler
from SearchEngine.searcher import *
from SearchEngine.conf import OUTPUT_FILENAME, CUR_WORK_DIRECTORY
from SearchEngine.web import app

WSE_DATA_DIR = CUR_WORK_DIRECTORY + "/tmp/data"
WSE_DATA_PATH = WSE_DATA_DIR + "/" + OUTPUT_FILENAME

INDEX_DIR = "IndexFiles.index"
WSE_INDEX_DIR = CUR_WORK_DIRECTORY + "/tmp/index"
WSE_INDEX_PATH = WSE_INDEX_DIR + "/" + INDEX_DIR

def run_deco(foo):
    def deco_foo():
        print "%s begin"%foo.__name__
        start_time = datetime.now()
        foo()
        end_time = datetime.now()
        print "%s done"%foo.__name__
        print "%s execute time: %s\n\n\n"%(foo.__name__, str(end_time - start_time))
    return deco_foo

@run_deco
def course_crawler():
    # start crawling
    crawler = CourseCrawler()
    crawler.start_crawl()

@run_deco
def course_indexer():
    init_course_index()

@run_deco
def run_web():
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    # crawler
    course_crawler()

    # indexer
    course_indexer()

    # run web server
    run_web()
