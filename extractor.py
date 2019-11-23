from bs4 import BeautifulSoup
import json

def period_into_range(period_list):
    if len(period_list) == 2:
        return list(range(int(period_list[0]), int(period_list[1])+1))
    else:
        return [int(x) for x in period_list]

def read_courses(html_filename, language):
    with open(html_filename) as courses_file:
        soup = BeautifulSoup(courses_file.read(), "html.parser")
        # 3,4 period data : 'courses.html'
        courses = []
        for x in soup.findAll("tr", {"role": "row"}):
            children = x.findChildren('td')
            if len(children) != 0:
                course_code, implementation_year = children[0].findAll('a')[0].contents[0].strip("\t\n").split()
                course_link = children[0].findAll('a')[0].attrs['href']
                course_name = children[1].findAll('a')[0].contents[0].strip("\n\t")
                course_credit = children[2].contents[0].replace("\t","").replace("\n","").replace("cr","")
                periods = [x.strip(" ") for x in children[3].contents[0].strip("\n\t").split("-")]
                periods = ['5' if x == "Kesä" else x for x in periods]
                subject = children[4].contents[0].strip("\n\t")
                course_obj = { 'course_code': course_code, 'implementation_year': implementation_year, 'course_link': course_link, 'credits': course_credit, 'subject': subject,
                               'course_name': course_name, 'periods': periods, 'language': language }
                courses.append(course_obj)
        return courses


en_courses = read_courses('courses_1_2.html', 'en') + read_courses('courses_3_4.html', 'en') + read_courses('courses_summer.html', 'en')
all_courses = []
for i in range(1,21):
    all_courses += read_courses(f'all_courses{i}.html', 'fi')
en_course_code = list(map(lambda d: d['course_code'], en_courses))
fi_courses = [x for x in all_courses if x["course_code"] not in en_course_code]
all_courses = en_courses + fi_courses

with open ("courses.json", 'w') as courses_out:
    json.dump(all_courses, courses_out)