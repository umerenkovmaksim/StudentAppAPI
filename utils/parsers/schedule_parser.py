import json

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def parse_schedules(url: str, save_path: str = None, save_file=False):
    headers = Headers(
        browser='chrome',
        os='mac',
        headers=True,
    )

    response = requests.get(url=url, headers=headers.generate(), verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    links = {}
    institutes = soup.select('.multicontent .content.row .col-12.content__block.content__block--structure .accordion')[0].select('.card')

    for institute in institutes:
        degrees = institute.select('.tabs-type-1.js-tabbed-block div div')
        institute_name = institute.select_one('h5 a').text.strip()
        links[institute_name] = {}

        for item in degrees:
            data = item.select_one('.col-12.content__block.content__block--file')
            if not data:
                continue
            schedule = data.select_one('a')
            degree = ''.join(filter(str.isdigit, data.text))
            links[institute_name][int(degree)] = 'https://www.timacad.ru/' + schedule.get('href')

        if not links[institute_name]:
            del links[institute_name]

    if not save_path and not save_file:
        return links
    paths = {}

    for institute, degrees in links.items():
        paths[institute] = {}
        for degree, schedule_link in degrees.items():
            file_path = save_path + schedule_link.split('/')[-1]
            with open(file_path, mode='wb') as file:
                file_content = requests.get(schedule_link).content
                file.write(file_content)
            paths[institute][degree] = file_path

    if save_file:
        with open('data/paths.json', 'w') as f:
            json.dump(paths, f, ensure_ascii=False)
    if save_path:
        return paths
    return links
