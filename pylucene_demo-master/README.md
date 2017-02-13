pylucene_demo
=============

####a simple pylucene_demo 

this demo contains two files: luceneInx.py and luceneQryMain.py
luceneInx.py is used for create a index of files
luceneQryMain.py ask for a query

基于Java的全文索引/检索引擎——Lucene

Lucene不是一个完整的全文索引应用，而是是一个用Java写的全文索引引擎工具包，它可以方便的嵌入到各种应用中实现针对应用的全文索引/检索功能。

Lucene的作者：Lucene的贡献者Doug Cutting是一位资深全文索引/检索专家，曾经是V-Twin搜索引擎(Apple的Copland操作系统的成就之一)的主要开发者，后在Excite担任高级系统架构设计师，目前从事于一些INTERNET底层架构的研究。他贡献出的Lucene的目标是为各种中小型应用程序加入全文检索功能。

Lucene的发展历程：早先发布在作者自己的www.lucene.com，后来发布在SourceForge，2001年年底成为APACHE基金会jakarta的一个子项目：http://jakarta.apache.org/lucene/

已经有很多Java项目都使用了Lucene作为其后台的全文索引引擎，比较著名的有：

Jive：WEB论坛系统；
Eyebrows：邮件列表HTML归档/浏览/查询系统，本文的主要参考文档“TheLucene search engine: Powerful, flexible, and free”作者就是EyeBrows系统的主要开发者之一，而EyeBrows已经成为目前APACHE项目的主要邮件列表归档系统。
Cocoon:基于XML的web发布框架，全文检索部分使用了Lucene
Eclipse:基于Java的开放开发平台，帮助部分的全文索引使用了Lucene

对于中文用户来说，最关心的问题是其是否支持中文的全文检索。但通过后面对于Lucene的结构的介绍，你会了解到由于Lucene良好架构设计，对中文的支持只需对其语言词法分析接口进行扩展就能实现对中文检索的支持。

