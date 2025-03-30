from sqlalchemy import select

from app.dao.base import BaseDAO
from app.students.models import Group, Student


class StudentDAO(BaseDAO):
    model = Student

class GroupDAO(BaseDAO):
    model = Group

    @classmethod
    async def get_institutes(cls, session, **filter_by):
        query = select(cls.model)
        query = query.filter_by(**filter_by).distinct(cls.model.institute)
        result = await session.execute(query)
        return [item.institute for item in result.scalars().all() if item.institute]
