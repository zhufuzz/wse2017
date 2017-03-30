#encoding=utf-8
import pdb

from bs4 import BeautifulSoup
from requests import Request
import re

from SearchEngine.utils import logger

from . import CrawlerBase, CRAWLER_URL

def trim(s):
    s = re.sub('\n', ' ', s)
    s = re.sub('\t', ' ', s)
    s = re.sub(' +', ' ', s)
    return s

class CourseCrawler(CrawlerBase):
    def __init__(self):
        """
        override the original init function, reset root_url
        """
        CrawlerBase.__init__(self, None, 1)

        years =  map(lambda x: str(x), range(2010, 2018))
        seasons = ["spring", "summer", "fall"]
        for year in years:
            for season in seasons:
                payload = {}
                payload["semester"] = season + '_' + year
                req = Request("GET","https://www.cs.nyu.edu/dynamic/courses/schedule/",params = payload)
                assembled_req = req.prepare()
                url = assembled_req.url

                url_description = CRAWLER_URL(url, 0, 0, True)
                self.add_new_url_to_list(url_description)

    @staticmethod
    def get_smester_from_url(url):
        try:
            payload = url.split("?")[1]
            return payload.split("=")[1]
        except Exception:
            return "unknown"

    def _process_content(self, content, url):
        soup = BeautifulSoup(content, "html.parser")
        # get all courses
        course_list = soup.find_all("li",id = re.compile("csci"))
        course_info_list = []

        for course in course_list:
            web_element = course.find_all("span")

            course_code = web_element[0].text
            course_name = web_element[1].text
            teacher = web_element[2].text.replace("Office Hours","")
            course_time = web_element[3].text
            classromm = web_element[4].text
            introduction = web_element[5].text
            try:
                course_url = web_element[0].a.get("href")
            except Exception:
                course_url = "unavailable "

            course_info = {"course_code": trim(course_code),
                    "course_name": trim(course_name),
                    "teacher": trim(teacher),
                    "course_time": trim(course_time),
                    "classromm": trim(classromm),
                    "introduction": trim(introduction),
                    "semster": trim(self.get_smester_from_url(url)),
                    "url":trim(course_url)}
            course_info_list.append(course_info)
        return course_info_list
