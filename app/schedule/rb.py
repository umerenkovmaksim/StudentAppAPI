from datetime import datetime


class RBLesson:
    def __init__(self, group_id: int | None = None,
                 date: str | None = None,
                 teacher_id: int | None = None):

        self.group_id = group_id
        self.date = date
        self.teacher_id = teacher_id
        self.day_of_week = self._get_day_of_week()
        self.split = self._get_split()

    def _get_day_of_week(self) -> int:
        if self.date:
            date_obj = datetime.strptime(self.date, "%Y-%m-%d")
            return date_obj.isoweekday() - 1
        return None

    def _get_split(self) -> list[int]:
        if self.date:
            date_obj = datetime.strptime(self.date, "%Y-%m-%d")
            week_number = date_obj.isocalendar()[1]
            return [0, 1] if week_number % 2 == 0 else [0, 2]
        return None

    def to_dict(self) -> dict:
        data = {
            'group_id': self.group_id,
            'day_of_week': self.day_of_week,
            'split': self.split,
            'teacher_id': self.teacher_id,
        }
        return {key: value for key, value in data.items() if value is not None}
