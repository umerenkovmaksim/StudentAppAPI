import json
import os
from http import HTTPStatus

import requests
from parsers.schedule_parser import parse_schedules
from pdf_extractor.parse_pdf_schedule import pdf_to_formatted_json

SCHEDULE_URL = 'https://www.timacad.ru/about/sveden/document/rezhim-zaniatii-obuchaiushchikhsia'
# API_URL = 'http://138.124.114.106:8000/'
API_URL = 'http://127.0.0.1:8000/'

def update_lessons(from_file=False):
    save_path = 'data/schedules/'
    current_dir = os.path.dirname(__file__)
    relative_path = os.path.join(current_dir, save_path)
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)

    if from_file:
        with open('data/paths.json') as f:
            paths = json.load(f)
    else:
        paths = parse_schedules(SCHEDULE_URL, relative_path, save_file=True)

    for institute, degrees in paths.items():
        for degree, path in degrees.items():
            lessons, groups = pdf_to_formatted_json(path, institute=institute, degree=degree)
            group_ids = []

            for group in groups:
                group_instance = requests.get(f'{API_URL}groups?short_name={group[0]}&degree={group[1]}').json()
                if not group_instance:
                    continue
                group_ids.append(group_instance[0]['id'])

            for group_id in group_ids:
                requests.delete(f'{API_URL}schedule/lessons?group_id={group_id}')

            res = requests.post(f'{API_URL}schedule/lessons', json=lessons)
            if res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
                with open('res.json', 'w') as f:
                    json.dump(res.json(), f, ensure_ascii=False)


if __name__ == '__main__':
    update_lessons(from_file=True)
