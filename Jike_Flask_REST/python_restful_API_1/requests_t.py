#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

#r = requests.get('http://127.0.0.1:5000/login', auth=('magigo', '123456'))
#print r.text

token ='bWFnaWdvOjAuOTYxMjQ1MjY5MzU1OjE0ODczOTk4MjMuNjQ='
r = requests.get('http://127.0.0.1:5000/test1', params={'token': token})
print r.text

# bWFnaWdvOjAuMzE4MTUxNTA1MjQ4OjE0MjU4MzkzMjMuODk=