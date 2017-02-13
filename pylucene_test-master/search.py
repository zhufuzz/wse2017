#coding: utf-8

import lucene
import csv

print "预处理"
INDEX_DIR = 'index'

lucene.initVM()
directory = lucene.SimpleFSDirectory(lucene.File(INDEX_DIR))
analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)

def search(q):
    """
    
    Arguments:
    - `q`:
    """
    print "查询字符串 %s."%(q)

    print "创建查询器"
    searcher = lucene.IndexSearcher(directory,True)

    query = lucene.QueryParser(lucene.Version.LUCENE_CURRENT,
                               'content',analyzer).parse(q)

    print "查询"
    results = searcher.search(query,None,3)
    
    score_docs = results.scoreDocs

    a = 0
    for score_doc in score_docs:
        doc = searcher.doc(score_doc.doc)
        print a,doc['content']
        a += 1
    
    
    
if __name__ == '__main__':
    print "hello world"
    query = "java"
    search(query)


