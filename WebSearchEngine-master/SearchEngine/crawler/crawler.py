#encoding=utf-8

from bs4 import BeautifulSoup
import requests, re, urlparse
from requests import Request
from robotparser import RobotFileParser

from SearchEngine.conf import REQUEST_TIMEOUT, ROBOTS_TXT_TIMEOUT, OUTPUT_FILENAME, CUR_WORK_DIRECTORY
from SearchEngine.utils import logger,mkdir_p

from . import Data2File_Handler

# error handling
WSE_ERROR_CODE_OK = 0
WSE_ERROR_REQUEST_BASE = 1000
WSE_ERROR_ROBOT_PARSE_BASE = 2000
WSE_ERROR_ADD_NEW_URL_BASE= 3000

# WSE_ERROR_REQUEST_BASE
WSE_ERROR_REQUEST_BAD_CONNECTION = WSE_ERROR_REQUEST_BASE + 1
WSE_ERROR_REQUEST_UNKNOWN_EXECEPTION = WSE_ERROR_REQUEST_BASE + 2

# WSE_ERROR_ROBOT_PARSE_BASE
WSE_ERROR_ROBOT_PARSE_GET_TXT_FILE = WSE_ERROR_ROBOT_PARSE_BASE + 1

# WSE_ERROR_ADD_NEW_URL_BASE
WSE_ERROR_ADD_NEW_URL_ALREADY_EXSIST = WSE_ERROR_ADD_NEW_URL_BASE + 1
WSE_ERROR_ADD_NEW_URL_ALREADY_CRAWLED = WSE_ERROR_ADD_NEW_URL_BASE + 2

WSE_DATA_DIR = CUR_WORK_DIRECTORY + "/tmp/data"
WSE_DATA_PATH = WSE_DATA_DIR + "/" + OUTPUT_FILENAME

#---------------------------------- data structure def -------------------------------------------------
class CRAWLER_URL:
    def __init__(self, url, depth, max_depth, is_leaf_node = False):
        self.url = url
        self.depth = depth
        self.max_depth = max_depth
        self.is_leaf_node = is_leaf_node

class TimeoutRobotFileParser(RobotFileParser):
    """
    add robot file parser with timeout
    """
    def __init__(self, url='', timeout=60):
        RobotFileParser.__init__(self, url)
        self.timeout = 1.0 * REQUEST_TIMEOUT / 1000
        self.__url = url

    def read(self):
        """Reads the robots.txt URL and feeds it to the parser."""
        try:
            f = requests.get(self.url, timeout=self.timeout)
        except requests.exceptions.ConnectionError:
            logger.error("connection error getting robots.txt <url: %s>"%self.__url)
            self.disallow_all = True
        except requests.exceptions.ConnectTimeout:
            logger.error("connection timeout getting robots.txt <url: %s>"%self.__url)
            self.disallow_all = True

        else:
            if f.status_code > 400:
                self.allow_all = True
            else:
                raw = f.content
                self.parse(raw.splitlines())

#---------------------------------- Crawler handler def -------------------------------------------------
class CrawlerBase:
    """
    Base Crawler can crawl url
    """
    def __init__(self, root_url, max_depth):
        """
        init the crawler instances
        @param: root_url is the root we deems as the base url
        @return: no return value
        @todo: 1. store mode, user can configure the result to be stored in either memory
               or disk
               2. modify params check
               3. configurable file handler type
        """
        if not isinstance(root_url, str):
            if root_url is None:
                logger.warning("root url is not None")
            else:
                logger.error("param @root_url is not string type")
                assert False
        if not isinstance(max_depth, int):
            logger.error("param @max_depth is not not int type")
            assert False
        if max_depth <= 0:
            logger.error("param @max_depth should be greater than 0")
            assert False

        #init robots.txt infomation
        self.__robots_managers = {}

        self.__crawled_urls = []
        self.__failed_urls = []
        self._uncrawled_urls = {}
        if root_url:
            url_description = CRAWLER_URL(root_url, 0, max_depth, False)
            self.add_new_url_to_list(url_description)

        #init data persistence module init
        mkdir_p(WSE_DATA_DIR)
        self.__file_handler = Data2File_Handler(WSE_DATA_PATH)
        self._write_data = self.__file_handler.save_result

    @property
    def failed_urls(self):
        return self.__failed_urls

    @property
    def crawled_urls(self):
        return self.__crawled_urls

    def __add_robot_parser(self, url):
        """
        add robot parser to crawler's dictionary
        """
        if not (isinstance(url, str) or isinstance(url, unicode)):
            logger.error("param @url is not string type")
            assert False

        parse_ret = urlparse.urlparse(url)
        hostname = parse_ret.hostname
        if hostname in self.__robots_managers:
            logger.warning("robots file of url<%s> has recorded"%url)
            return WSE_ERROR_CODE_OK
        else:
            robots_txt_url = parse_ret._replace(path="robots.txt").geturl()

            try:
                robot_manager = TimeoutRobotFileParser(robots_txt_url)
                robot_manager.read()
                self.__robots_managers[hostname] = robot_manager
                logger.info("robots file of url<%s> has recorded"%url)
                return WSE_ERROR_CODE_OK

            except IOError:
                logger.error("robots file <url: %s>can not be found"%robots_txt_url)
                return WSE_ERROR_ROBOT_PARSE_GET_TXT_FILE

    def __can_crawl_url(self, url):
        """
        Judge if the given url can be crawled according to the robots.txt
        @note: if robots.txt is inreachable, return False to the given urls
        """
        if not (isinstance(url, unicode) or isinstance(url, str)):
            logger.error("param @url is not string type")
            assert False

        parse_ret = urlparse.urlparse(url)
        hostname = parse_ret.hostname
        if not hostname in self.__robots_managers:
            ret = self.__add_robot_parser(url)
            if not ret is WSE_ERROR_CODE_OK:
                return False

        robot_manager = self.__robots_managers[hostname]
        can_fetch = robot_manager.can_fetch("*", url.encode("utf-8"))
        return can_fetch

    def _clean_uncrawled_urls(self):
        """
        clean all uncrawled urls
        """
        self._uncrawled_urls.clear()
        logger.info("clean all uncrawled urls")

    @staticmethod
    def normalize_url(url, host_url):
        url = url.strip()
        host_url = host_url.strip()

        absolute_link_match = re.compile("^https?://")
        if absolute_link_match.match(url):
            return url

        anchor_match = re.compile("^#")
        if anchor_match.match(url):
            return None

        relative_match = re.compile("^/")
        if relative_match.match(url):
            if not absolute_link_match.match(host_url):
                logger.error("Normalize_url: host <%s> illegal"%host_url)
                return None
            parse_ret = urlparse.urlparse(host_url)
            # hostname is pattern like www.cnblogs.com
            hostname = parse_ret.hostname
            return "http://"+ hostname + url

    @staticmethod
    def normalize_urls(url, host_url = None):
        """
        1. filter out href started with "#"
        2. complete incomplete url
        """
        if isinstance(url, list) or isinstance(url, tuple):
            ret = []
            for u in url:
                u = CRAWLER_URL.normalize_url(u, host_url)
                if u:
                    ret.append(u, host_url)
            return ret
        if isinstance(url, str) or isinstance(url,unicode):
            return self.__url_filter(url, host_url)
        else:
            return None

    def add_new_url_to_list(self, url_description):
        """
        add new url to list
        this function could be called directly by the user to process some corner cases
        robots.txt detection is intergrated inside this function
        @todo: params check
        """
        url = url_description.url
        if url in self._uncrawled_urls:
            return WSE_ERROR_ADD_NEW_URL_ALREADY_EXSIST
        if url in self.__crawled_urls:
            return WSE_ERROR_ADD_NEW_URL_ALREADY_CRAWLED
        if not self.__can_crawl_url(url):
            logger.info("url disallowed by robot.txts <url: %s>"%url)

        self._uncrawled_urls[url] = url_description
        logger.debug("add new url to list <url: %s, cur_depth: %d, max_depth: %d, is_leaf: %s>"
                %(url, url_description.depth, url_description.max_depth, url_description.is_leaf_node))
        return WSE_ERROR_CODE_OK

    def start_crawl(self):
        """
        start the main crawling process
        @param: max_url_cnt is the urls that would be crawled at a single time, default value is infinite
        @return:
        @todo: max_url_cnt related code ..
        """
        while len(self._uncrawled_urls) != 0:
            success_cnt = 0
            fail_cnt = 0

            url_item = self._uncrawled_urls.popitem()
            url_description = url_item[1]
            crawl_url = url_description.url
            cur_depth = url_description.depth
            max_depth = url_description.max_depth
            is_leaf = url_description.is_leaf_node

            logger.debug("processing <url: %s>...."%crawl_url)

            # 1. get content
            ret = self.request_url(crawl_url)
            if (ret[0] != WSE_ERROR_CODE_OK):
                logger.error("get content fail <url: %s>, <ret %d>"%(crawl_url, ret[0]))
                fail_cnt += 1
                self.__failed_urls.append(crawl_url)
                continue
            else:
                success_cnt += 1
                self.__crawled_urls.append(crawl_url)
                logger.debug("get content done <url: %s>...."%crawl_url)

            # 2. process content
            web_content = ret[1]
            process_data_list = self._process_content(web_content, crawl_url)

            # 3. store processed data
            self._write_data(process_data_list)

            # 4. get hyper links and add them to lists
            cur_depth += 1
            if (not is_leaf) and (cur_depth < max_depth):
                urls = self.get_hyper_links(web_content)
                for url in urls:
                    url["url"] = self.normalize_url(url["url"], crawl_url)
                    if url["url"]:
                        new_url_description = CRAWLER_URL(url["url"], cur_depth, max_depth, url["is_leaf_node"])
                        self.add_new_url_to_list(new_url_description)

            # done:
            logger.info("<url %s> crawling done, success_cnt:%d fail_cnt:%d"%(crawl_url, success_cnt, fail_cnt))

    def _process_content(self, content, url=None):
        """
        need to be overrided
        """
        return {"content": content}

    def get_hyper_links(self, content, match_str=""):
        """
        get hyper links
        can be rewrite to implement specific hyperlink extract needs. In default case, no link is leaf node
        @note: may extract incomplete/relative url
        @todo: 1. add exclude str, and make it together with params match_str in a kargs
               2. modify params check method
        """
        if not isinstance(content, str):
            logger.error("content is not string type")
            assert False

        links = []

        soup = BeautifulSoup(content, "html.parser")
        result_set = soup.find_all('a',text = re.compile(match_str))
        for link in result_set:
            try:
                url = link["href"]
            except KeyError:
                logger.debug("can't find href info in a tag <%s>"%(str(link)))
                continue
            else:
                links.append({"url":url, "is_leaf_node":False})
        return links

    def request_url(self, url, timeout=2000):
        """
        request given url within given timeout upper limit
        @param:
                timeout: unit is ms
        @return: return a two_tuples result, result[0] is the return code
                 if return code is 0, then the function works while and result[1]
                 is the content of url
         """
        try:
            response = requests.get(url, timeout = 1.0/1000*timeout)
            if response.status_code == 200:
                return WSE_ERROR_CODE_OK, response.content
            else:
                return WSE_ERROR_REQUEST_BAD_CONNECTION, None

        except Exception,e:
            logger.error("exception when requesting url <Exception: %s>"%str(e))
            return WSE_ERROR_REQUEST_UNKNOWN_EXECEPTION, None
