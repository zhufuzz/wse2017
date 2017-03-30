#encoding
import re
from datetime import datetime
from flask import Flask, render_template, request
from SearchEngine.searcher import CourseSearcher

from SearchEngine.conf import CUR_WORK_DIRECTORY

INDEX_DIR = "IndexFiles.index"
WSE_INDEX_DIR = CUR_WORK_DIRECTORY + "/tmp/index"
WSE_INDEX_PATH = WSE_INDEX_DIR + "/" + INDEX_DIR

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route('/search/')
def search():
    q = request.args.get('inputword')
    if q is None:
        return render_template('main.html')

    course_searcher = CourseSearcher(WSE_INDEX_PATH)

    # 1. filter illegal characters
    q = re.sub("[^\w]"," ", q)
    q = re.sub("[\s]+", " ", q)

    # 2. search in filed introduction and teacher
    start = datetime.now()
    courses_info = course_searcher.search_course(q)
    course_info_by_teacher = course_searcher.search_course(q, field = "teacher")
    for course_info in course_info_by_teacher:
        if not course_info in courses_info:
            courses_info.append(course_info)
    end = datetime.now()

    if (len(courses_info) == 0):
        return render_template('no_result.html', keyword = q)
    else:
        return render_template('display_new.html', courses_info = courses_info, keyword = q
                , search_times=(end-start).total_seconds(), cnt=len(courses_info))

if __name__ == '__main__':
    app.run()

