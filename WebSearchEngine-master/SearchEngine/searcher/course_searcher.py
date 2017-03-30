#encoding=utf-8
#!/usr/bin/env python

import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

from SearchEngine.conf import OUTPUT_FILENAME, CUR_WORK_DIRECTORY
from SearchEngine.utils import logger,mkdir_p

INDEX_DIR = "IndexFiles.index"
WSE_INDEX_DIR = CUR_WORK_DIRECTORY + "/tmp/index"
WSE_INDEX_PATH = WSE_INDEX_DIR + "/" + INDEX_DIR

class CourseSearcher():
    def __init__(self, index_file_path):
        if lucene.getVMEnv() is None:
            lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        store = SimpleFSDirectory(Paths.get(index_file_path))
        self.__searcher = IndexSearcher(DirectoryReader.open(store))
        self.__analyzer = StandardAnalyzer()

    def __del__(self):
        del self.__searcher

    def __get_info_by_doc(self, doc):
        info = {}
        info["name"] = doc.get("name")
        info["ID"] = doc.get("ID")
        info["url"] = doc.get("url")
        info["semester"] = doc.get("semester")
        info["intro"] = doc.get("intro")
        info["teacher"] = doc.get("teacher")
        return info

    def search_course(self, keyword, field = "intro", is_print = False):
        print "Searching for:", keyword
        query = QueryParser(field, self.__analyzer).parse(keyword)
        scoreDocs = self.__searcher.search(query, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        ret = []
        for scoreDoc in scoreDocs:
            doc = self.__searcher.doc(scoreDoc.doc)
            info = self.__get_info_by_doc(doc)
            ret.append(info)
            if (is_print):
                print info
        return ret
