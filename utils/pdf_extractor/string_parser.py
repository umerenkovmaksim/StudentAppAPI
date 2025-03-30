import re


def parse_lesson_string(line: str) -> list[str]:
    line = line.replace('ё', 'е').replace('Ë', 'Е')
    location_pattern = re.compile(r'\s*(\d+-[a-zA-Zа-яА-Я0-9]+)', re.UNICODE)
    teacher_pattern = re.compile(r'[А-Я]+\s[А-Я]\.[А-Я]\.', re.UNICODE)

    location_matches = list(location_pattern.finditer(line))
    teacher_matches = list(teacher_pattern.finditer(line))

    locations = [match.group(1) for match in location_matches]
    teachers = [match.group() for match in teacher_matches]

    for match in reversed(location_matches + teacher_matches):
        line = line[:match.start()] + line[match.end():]

    max_len = max(len(locations), len(teachers), 1)
    locations.extend([None] * (max_len - len(locations)))
    teachers.extend([None] * (max_len - len(teachers)))

    line = line.strip()
    return [locations, teachers, line]
