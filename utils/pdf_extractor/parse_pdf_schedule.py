import logging

import pdfplumber
from pdf_extractor.string_parser import parse_lesson_string

DAYS_OF_WEEK = {
    'понедельник': 0,
    'вторник': 1,
    'среда': 2,
    'четверг': 3,
    'пятница': 4,
    'суббота': 5,
    'воскресенье': 6,
}

def format_raw_data(data):
    for index, row in enumerate(data):
        new_data = [row[0]]
        return_string = row[0] and row[0][-2:] == '\n'
        for elem in row[1:]:
            if return_string:
                new_data[-1] += elem
            else:
                new_data.append(elem)

            return_string = elem and elem[-2:] == '\n'

        data[index] = new_data

    return data

def parse_pdf_schedule(pdf_path):
    schedule_data = []
    logging.info(f"Parsing: {pdf_path}...")
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            data = []
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    transposed_table = list(zip(*table))
                    for row in transposed_table[::-1]:
                        data.append(row)
            else:
                data.append(page.extract_text())

            schedule_data.append(data)

    return schedule_data

def convert_data_to_json(data, institute, degree):
    objects = []
    groups = set()

    for page in data:
        days_of_week = []
        cur = -1
        for elem in page.pop(-1)[1:]:
            if elem is not None:
                cur += 1
                days_of_week.append(cur)
            else:
                days_of_week.append(cur)

        times = page.pop(-1)

        for group in page:
            group_name = group[0]
            if group_name in {'Часы', 'Дни'}:
                continue
            for index, lesson in enumerate(group):
                if index == 0:
                    continue
                lesson_time = times[index] or times[index - 1]
                time_from, time_to = (
                    lesson_time
                    .replace('.', ':')
                    .replace('\n', '')
                    .split('-')
                )
                split = 0
                if times[index] and index + 1 < len(times) and times[index + 1] is None and group[index + 1] is not None:
                    split = 1
                elif not times[index]:
                    split = 2

                if lesson:
                    parsed_data = parse_lesson_string(lesson)
                    lesson_name = parsed_data[2]
                    for i in range(len(parsed_data[0])):
                        building, cabinet = parsed_data[0][i].split('-') if parsed_data[0] and parsed_data[0][i] else (-1, '-1')
                        groups.add((group_name, degree, institute))
                        lesson_data = {
                            'name': lesson_name,
                            'group': {
                                'short_name': group_name,
                                'degree': degree,
                                'institute': institute,
                            },
                            'time_from': time_from,
                            'time_to': time_to,
                            'split': split,
                            'day_of_week': days_of_week[index - 1],
                            'building': int(building),
                            'cabinet': cabinet,
                        }
                        if teacher := parsed_data[1][i]:
                            lesson_data['teacher'] = {
                                'short_name': teacher,
                            }
                        objects.append(lesson_data)


    return objects, groups

def pdf_to_formatted_json(pdf_path, institute, degree):
    parsed_data = parse_pdf_schedule(pdf_path)
    formatted_data = format_raw_data(parsed_data)
    json_data, groups = convert_data_to_json(formatted_data, institute, degree)

    return json_data, groups

# pdf_file_path = "/Users/umerenkovmaksim/VSCodeProjects/StudentAppAPI/utils/data/schedules/1737703943_ieiu-1.pdf"

# json_data, groups = pdf_to_formatted_json(pdf_file_path, 'IEIU', 1)
# with open('/Users/umerenkovmaksim/VSCodeProjects/StudentAppAPI/utils/pdf_extractor/uploads/schedule.json', mode='w') as json_file:
#     json.dump(json_data, json_file, ensure_ascii=False)
# with open('/Users/umerenkovmaksim/VSCodeProjects/StudentAppAPI/utils/pdf_extractor/uploads/groups.json', mode='w') as json_file:
#     json.dump(groups, json_file, ensure_ascii=False)
