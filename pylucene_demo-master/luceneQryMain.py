#!/usr/bin/env python
#encoding: utf-8
#
# Copyright [current year] the Melange authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
本模块用于完成Lucene的检索
luceneIndexer(docdir,indir):IndexDocuments from a directory.
luceneRetriver(queryString)：执行一次查询，queryString为搜索句子
"""
# import lucene
# from lucene import \
#     SimpleFSDirectory, System, File, \
#     Document, Field, StandardAnalyzer, IndexSearcher, Version, QueryParser

import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

import sys, os, lucene

from string import Template
from datetime import datetime
from getopt import getopt, GetoptError

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory

def luceneRetriver(queryString):
	lucene.initVM()
	#指明索引所处位置
	indexDir = "/Users/tzh/PycharmProjects/wse2017/pylucene_test/index"
	dir = SimpleFSDirectory(Paths.get(indexDir))
	analyzer = StandardAnalyzer()
	# searcher = IndexSearcher(dir)
	searcher = IndexSearcher(DirectoryReader.open(dir))
	query = QueryParser("text", analyzer).parse(queryString)
	MAX = 1000
	#最多记录数
	hits = searcher.search(query, MAX)
	print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
	for hit in hits.scoreDocs:
		print hit.score, hit.doc, hit.toString()
		doc = searcher.doc(hit.doc)
		print doc.get("path").encode("utf-8")

if __name__ == "__main__":
    luceneRetriver("latex3")