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


def run_web():
    app.run()

def unit_test_deco(foo):
    def deco_foo():
        print "%s begin"%foo.__name__
        start_time = datetime.now()
        foo()
        end_time = datetime.now()
        print "%s done"%foo.__name__
        print "%s execute time: %s\n\n\n"%(foo.__name__, str(end_time - start_time))
    return deco_foo

@unit_test_deco
def test_course_crawler():
    # start crawling
    crawler = CourseCrawler()
    crawler.start_crawl()

@unit_test_deco
def index_test():
    try:
        course_indexer = CourseIndexer(WSE_INDEX_PATH)
        course_indexer.index_course({"name":"web search engine", "url":"www.baidu.com"})
        course_indexer.index_course({"name":"programming language", "url":"www.google.com"})
        del course_indexer
    except Exception, e:
        print "Failed: ", e
        raise e

@unit_test_deco
def index_course_test():
    init_course_index()

@unit_test_deco
def searcher_test():
    try:
        course_searcher = CourseSearcher(WSE_INDEX_PATH)
        course_searcher.search_course("Benjamin", "teacher")
        del course_searcher
    except Exception, e:
        print "Failed: ", e
        raise e
