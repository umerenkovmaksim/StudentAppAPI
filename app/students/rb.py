class RBStudent:
    def __init__(self, id: int | None = None,  # noqa: PLR0913
                 student_id: int | None = None,
                 telegram_id: int | None = None,
                 email: str | None = None,
                 first_name: str | None = None,
                 last_name: str | None = None,
                 group_id: int | None = None):
        self.id = id
        self.student_id = student_id
        self.telegram_id = telegram_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.group_id = group_id

    def to_dict(self):
        data = {
            'id': self.id,
            'student_id': self.student_id,
            'telegram_id': self.telegram_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'group_id': self.group_id,
        }
        filtered_data = {}
        for key, value in data.items():
            if value is not None:
                filtered_data[key] = value
        return filtered_data


class RBGroup:
    def __init__(self, short_name: str | None = None,
                 institute: str | None = None,
                 degree: int | None = None,
                 major: str | None = None):
        self.short_name = short_name
        self.institute = institute
        self.degree = degree
        self.major = major

    def to_dict(self):
        data = {
            'short_name': self.short_name,
            'institute': self.institute,
            'degree': self.degree,
            'major': self.major,
        }
        filtered_data = {}
        for key, value in data.items():
            if value is not None:
                filtered_data[key] = value

        return filtered_data
