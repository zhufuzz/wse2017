#encoding=utf-8
#!/usr/bin/env python

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory

from SearchEngine.conf import OUTPUT_FILENAME, CUR_WORK_DIRECTORY
from SearchEngine.utils import logger,mkdir_p

WSE_DATA_DIR = CUR_WORK_DIRECTORY + "/tmp/data"
WSE_DATA_PATH = WSE_DATA_DIR + "/" + OUTPUT_FILENAME

INDEX_DIR = "IndexFiles.index"
WSE_INDEX_DIR = CUR_WORK_DIRECTORY + "/tmp/index"
WSE_INDEX_PATH = WSE_INDEX_DIR + "/" + INDEX_DIR

class CourseIndexer(object):
    def __init__(self, index_file_path):
        if lucene.getVMEnv() is None:
            lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        mkdir_p(index_file_path)

        store = SimpleFSDirectory(Paths.get(index_file_path))
        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.__writer = IndexWriter(store, config)

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(True)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)
        self.__info_field = t1

        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(False)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        self.__url_field = t2

    def __del__(self):
        self.__writer.commit()
        self.__writer.close()

    def index_course(self, course_info):
        try:
            doc = Document()
            if "name" in course_info:
                name = course_info["name"]
                doc.add(Field("name", name, self.__info_field))

            if "url" in course_info:
                url = course_info["url"]
                doc.add(Field("url", url, self.__url_field))

            if "semester" in course_info:
                semester = course_info["semester"]
                doc.add(Field("semester", semester, self.__info_field))

            if "intro" in course_info:
                intro = course_info["intro"]
                doc.add(Field("intro", intro, self.__info_field))

            if "ID" in course_info:
                ID = course_info["ID"]
                doc.add(Field("ID", ID, self.__url_field))

            if "teacher" in course_info:
                teacher = course_info["teacher"]
                doc.add(Field("teacher", teacher, self.__info_field))

            self.__writer.addDocument(doc)
        except Exception, e:
            print "Failed in indexDocs:", e

def parse_courses(file_name):
    courses_info = []
    f = open(file_name,'rb')
    while True:
        line = f.readline()
        course_info = {}
        if len(line) is 0:
            break

        info = line.split(",")
        if (len(info) != 9):
            pdb.set_trace()
        # hardcode here
        course_info["url"] = info[0]
        course_info["name"] = info[1]
        course_info["semester"] = info[2]
        course_info["intro"] = info[4].replace("_",",")
        course_info["ID"] = info[5]
        course_info["teacher"] = info[6]
        courses_info.append(course_info)

    return courses_info

def init_course_index():
    courses_info = parse_courses(WSE_DATA_PATH)

    try:
        course_indexer = CourseIndexer(WSE_INDEX_PATH)
        for info in courses_info:
            course_indexer.index_course(info)

        print "index %d courses information"%len(courses_info)
        del course_indexer
    except Exception, e:
        print "Failed: ", e
        raise e
