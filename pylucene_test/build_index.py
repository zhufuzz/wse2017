#coding: utf-8

import lucene
import csv


import sys, os, lucene, threading, time
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory

print "预处理"
INDEX_DIR = '/Users/tzh/PycharmProjects/wse2017/pylucene_test/index'

lucene.initVM()
directory = SimpleFSDirectory(Paths.get(INDEX_DIR))
analyzer = StandardAnalyzer()

def get_data():
    """
    """
    f = open("sub_train.csv")
    reader = csv.reader(f)

    data = []
    
    for row in reader:
        data.append((row[0]+" "+row[1],row[2]))

    return data

def build_index():
    """
    """
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(directory,config)

    data = get_data()
    print "数据个数:",len(data)
    
    
    t1 = FieldType()
    t1.setStored(True)
    t1.setTokenized(False)
    t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    t2 = FieldType()
    t2.setStored(False)
    t2.setTokenized(True)
    t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    
    
    for content,tag in data:
        doc = Document()
        
        # doc.add(Field('content',content,Field.Store.YES,
        #                      Field.Index.ANALYZED))
        # doc.add(Field('tag',tag,Field.Store.YES,
        #                      Field.Index.NOT_ANALYZED))

        doc = Document()
        doc.add(Field("content", content, t1))
        doc.add(Field("tag", tag, t1))
        

            
        writer.addDocument(doc)

    print "写引擎优化"
#    writer.optimize()
    writer.close()

    
    
    
if __name__ == '__main__':
    print "hello world"
    build_index()


