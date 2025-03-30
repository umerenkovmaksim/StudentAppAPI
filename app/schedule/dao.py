from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.schedule.models import Lesson, Teacher
from app.students.dao import GroupDAO


class LessonDAO(BaseDAO):
    model = Lesson

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        async with session.no_autoflush():
            teacher_data = values.pop('teacher', None)
            if teacher_data:
                teacher, _ = await TeacherDAO.get_or_create(session, **teacher_data)
                values['teacher_id'] = teacher.id

            group_data = values.pop('group', None)
            if group_data:
                group, _ = await GroupDAO.get_or_create(session, **group_data)
                values['group_id'] = group.id

            instance = cls.model(**values)
            session.add(instance)
            await session.commit()
            return instance

    @classmethod
    async def add_many(cls, session: AsyncSession, items):
        objects = []
        for item in items:
            teacher_data = item.pop('teacher', None)
            if teacher_data:
                teacher, _ = await TeacherDAO.get_or_create(session, **teacher_data)
                item['teacher_id'] = teacher.id

            group_data = item.pop('group', None)
            if group_data:
                group, _ = await GroupDAO.get_or_create(session, **group_data)
                item['group_id'] = group.id
            new_instance = cls.model(**item)
            session.add(new_instance)
            objects.append(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return objects

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model)
        if split := filter_by.get('split'):
            del filter_by['split']
            query = query.filter(Lesson.split.in_(split))
        query = query.filter_by(**filter_by)
        result = await session.execute(query.options(selectinload(Lesson.teacher)))
        return result.scalars().all()


class TeacherDAO(BaseDAO):
    model = Teacher
