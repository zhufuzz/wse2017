#encoding=utf-8
import os, re, subprocess, pdb, sys
from bs4 import BeautifulSoup as bs
from numpy import zeros, ones
from numpy.linalg import norm
from math import log

HTML_PATTERN = re.compile("((html)|(htm))$")
EM_TAG_NAME = ["h1", "H1", "h2", "H2", "h3", "H3", "h4", "H4",
                "em", "EM", "b", "B"]

def get_urls(content):
    soup = bs(content, "html.parser")
    result_set = soup.find_all("a")
    ret = {}
    for result in result_set:        
        remote_url = result.get("href")
        if remote_url in ret:
            links = ret[remote_url]
        else:
            links = 0

        links += 1
        for tag in result.parents:
            if tag.name in EM_TAG_NAME:
                links += 1
        ret[remote_url] = links
    return ret

def walk_dir(dir_name):
    for root,dirs,files in os.walk(dir_name):
        for f in files:
            yield os.path.join(root, f)

def get_word_count(file_name):
    try:
        stdout = subprocess.check_output(['wc','-w', file_name])
    except Exception,ex:
        print Exception,":",ex
        return 0
    stdout = stdout.strip().split(" ")
    return int(stdout[0])

def get_urls_info(dir_name):
    
    files = []
    sorted_urls = []
    for file_path in walk_dir(dir_name):
        files.append(file_path)
    files.sort()

    urls = {}
    for file_path in files:
        if not HTML_PATTERN.search(file_path):
            continue
        local_url_name = file_path.split("/")[-1]
        sorted_urls.append(local_url_name)
        try:
            f = open(file_path, 'rb')       
            content = f.read()
        except:
            print "exeption in read file %s"%file_path
            continue

        url_info = {}
        url_info["outlinks"] = get_urls(content)
        url_info["number"] = len(urls)
        url_info["word_cnt"] = get_word_count(file_path)
        url_info["base_importance"] = 0
        
        # should exclude local_url itself
        if local_url_name in url_info["outlinks"]:
            del url_info["outlinks"][local_url_name]

        urls[local_url_name] = url_info
    
    return urls, sorted_urls

def norm_base_importance(urls):
    total = 0
    for local_url, url_info in urls.items():
        url_info["base_importance"] = log(url_info["word_cnt"])
        total += url_info["base_importance"]

    for local_url, url_info in urls.items():        
        url_info["base_importance"] /= total
        # print local_url, url_info["base_importance"]

def del_outter_links(urls):
    for local_url, url_info in urls.items():
        if len(urls[local_url]["outlinks"]) == 0:
            continue
        for url,weight in url_info["outlinks"].items():
            if not url in urls:
                del url_info["outlinks"][url]
                continue

def get_links_mat(urls, F=0.7):
    if len(urls) < 2:
        print "we need to get more than 2 pages to calculate the rank\n"
        return None
    
    dim = len(urls)
    url_access_mtx = zeros(dim*dim).reshape(dim,dim)

    # 1. calcuate link matrix
    for local_url, url_info in urls.items():
        outlink_cnt = len(urls[local_url]["outlinks"])
        lo = url_info["number"]
        
        if outlink_cnt == 0:
            #deal with end links 
            for url in urls:
                # should exclude local_url itself
                if url == local_url:
                    continue
                re = urls[url]["number"]
                url_access_mtx[re, lo] += F/(len(urls) - 1)

        else:
            total_weight = 0
            for url,weight in url_info["outlinks"].items():
                total_weight += weight
            total_weight /= F

            for url,weight in url_info["outlinks"].items():                
                re = urls[url]["number"]
                url_access_mtx[re, lo] = weight/float(total_weight)

    # 2. add inherit value
    for local_url, url_info in urls.items():
        lo = url_info["number"]
        inherit_value = 0.3*url_info["base_importance"]
        # inherit_value = (1.0-F)/dim
        for re in range(dim):
            url_access_mtx[lo, re] += inherit_value
    
    return url_access_mtx

def cal_importance(a):
    dim = a[0].size
    b = ones(dim)
    b *= 1.0/dim

    it = 0
    while (True):
        it += 1;
        b_ = b
        b = a.dot(b)
        if (norm(b-b_)<0.000001):
            break

    print "iteration time: %d"%it
    return b

def usage():
    print "usage: process.py [file_name]"

if __name__ == "__main__": 
    if (len(sys.argv) < 2):
        usage()
        exit(0)

    urls, sorted_urls = get_urls_info(sys.argv[1])
    norm_base_importance(urls)
    del_outter_links(urls)
    url_access_mtx = get_links_mat(urls)
    b = cal_importance(url_access_mtx)
    idx = 0
    for url in sorted_urls:
        print url, b[idx]
        idx = idx + 1
