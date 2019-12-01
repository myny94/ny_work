#!/usr/bin/env python3.7

from bs4 import BeautifulSoup
import json
from os import listdir


def period_into_range(period_list):
    if len(period_list) == 2:
        return list(range(int(period_list[0]), int(period_list[1])+1))
    else:
        return [int(x) for x in period_list]


def read_courses(html_filename, language):
    with open(html_filename) as courses_file:
        soup = BeautifulSoup(courses_file.read(), "html.parser")
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
                course_obj = {
                    'course_code': course_code,
                    'implementation_year': implementation_year,
                    'course_link': course_link,
                    'credits': course_credit,
                    'subject': subject,
                    'course_name': course_name,
                    'periods': periods,
                    'language': language
                }
                courses.append(course_obj)
        return courses


def main():
    en_htmls = listdir('en')
    en_courses = []
    for html in en_htmls:
        en_courses += read_courses(f'en/{html}', 'en')

    en_course_codes = [course["course_code"] for course in en_courses]

    fi_htmls = listdir('fi')
    fi_courses = []
    for html in fi_htmls:
        fi_courses += read_courses(f'fi/{html}', 'fi')

    fi_courses_no_duplicates = [x for x in fi_courses if x["course_code"] not in en_course_codes]
    all_courses = en_courses + fi_courses_no_duplicates
    all_courses = list({v['course_code']:v for v in all_courses}.values())

    with open ("courses.json", 'w') as courses_out:
        json.dump(all_courses, courses_out)


if __name__ == "__main__":
    main()
