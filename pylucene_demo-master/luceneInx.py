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
本模块用于完成Lucene的初始化
luceneIndexer(docdir,indir):IndexDocuments from a directory.
"""
import os,sys,glob
import lucene
import sys, os, lucene, threading, time
from lucene import SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, IndexWriter, Version,IndexWriterConfig,FieldInfo


"""Example of Indexing with PyLucene 3.0
参考：http://blog.csdn.net/fan_hai_ping/article/details/7966461
"""

def luceneIndexer(docdir,indir):
	""" IndexDocuments from a directory.
	Args:
		docdir:文档所在文件夹
		indir:索引存放文件夹
	Returns:
		无返回值
	说明：
	FieldType().setStored=as-is value stored in the Lucene index
	FieldType().setTokenized=field is analyzed using the specified Analyzer - the tokens emitted are indexed
	FieldType().Indexed = the text (either as-is with keyword fields, or the tokens from tokenized fields) is made searchable (aka inverted)
	FieldType().Vectored = term frequency per document is stored in the index in an easily retrievable fashion.
	"""
	
	"""#类型1属性：对于需要检索，需要返回显示setStored(True)
	type1 = FieldType()
	type1.setIndexed(True)
	type1.setStored(True)
	type1.setTokenized(False)
	type1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
	#类型2属性：对于不用返回显示，但是需要进行检索的字段。这里我认为文本内容（content）是这一种的，通常例如文件的META信息。
	type2 = FieldType()
	type2.setIndexed(True)
	type2.setStored(False)
	type2.setTokenized(True)
	type2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)"""
	
	lucene.initVM()
	DIRTOINDEX= docdir
	INDEXIDR= indir
	indexdir= SimpleFSDirectory(File(INDEXIDR))
	analyzer= StandardAnalyzer(Version.LUCENE_30)
	#用指定的语言分析器构造一个新的写索引器.
	index_writer= IndexWriter(indexdir,analyzer,True,IndexWriter.MaxFieldLength(512))
	for tfile in glob.glob(os.path.join(DIRTOINDEX,'*.txt')):
	    #print "Indexing: "
		print "Indexing:", tfile;
		document = Document()
		content = open(tfile,'r').read()
		#类型使用方式
		#doc.add(Field("path", tfile, type1))
		
		#文档新增字段（Field）{字段名："text",存储：“YES”,索引:"YES"}
		document.add(Field("text",content,Field.Store.YES,Field.Index.ANALYZED))
		document.add(Field("path",tfile,Field.Store.YES,Field.Index.ANALYZED))
		index_writer.addDocument(document)
		print "Done: ", tfile
	index_writer.optimize()
	print index_writer.numDocs()
	index_writer.close()

if __name__ == "__main__":
	docdir="C:\input"
	indir="C:\index"
	luceneIndexer(docdir,indir)