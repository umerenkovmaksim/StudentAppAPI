from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schedule.dao import LessonDAO, TeacherDAO
from app.schedule.rb import RBLesson
from app.schedule.schemas import SLesson, SLessonAdd, STeacher

router = APIRouter(prefix='/schedule', tags=['Расписание'])

@router.get('/lessons', summary='Получить все пары')
async def get_lessons(request_body: RBLesson = Depends(), session: AsyncSession = Depends(get_db)) -> list[SLesson]:
    return await LessonDAO.find_all(session=session, **request_body.to_dict())

@router.delete('/lessons', summary='Удалить пары по фильтру')
async def delete_lessons(request_body: RBLesson = Depends(), session: AsyncSession = Depends(get_db)) -> dict:
    check = await LessonDAO.delete(session=session, **request_body.to_dict())
    if check:
        return {'message': f'{len(check) if isinstance(check, list) else 1} lesson(s) was deleted'}
    return {'error': 'Invalid data'}

@router.get('/lessons/{id}', summary='Получить пару по ID')
async def get_lesson_by_id(id: int, session: AsyncSession = Depends(get_db)) -> SLesson | None:
    return await LessonDAO.find_one_or_none_by_id(session=session, id=id)

@router.post('/lessons', summary='Добавить пару(ы)')
async def add_lessons(lesson: SLessonAdd | list[SLessonAdd], session: AsyncSession = Depends(get_db)) -> dict:
    if isinstance(lesson, list):
        check = await LessonDAO.add_many(session=session, items=(item.model_dump() for item in lesson))
        if check:
            return {'message': f'{len(check)} lesson(s) was added'}
        return {'error': 'Invalid data'}
    check = await LessonDAO.add(session=session, **lesson.model_dump())
    if check:
        return SLesson(**check.__dict__).model_dump()
    return {'error': 'Invalid data'}

@router.patch('/lessons/{id}', summary='Обновить данные о паре')
async def update_lesson(id: int, request_body: RBLesson = Depends(), session: AsyncSession = Depends(get_db)) -> SLesson:
    check = await LessonDAO.update(session=session, filter_by={'id': id},
                                   **request_body.to_dict())
    if check:
        return {'message': f'{check} lines was updated'}
    return {'error': 'Invalid data'}

@router.delete('/lessons/{id}', summary='Удалить данные о паре')
async def delete_lesson(id: int, session: AsyncSession = Depends(get_db)) -> dict:
    check = await LessonDAO.delete(session=session, id=id)
    if check:
        return {'message': 'Object wasdeleted'}
    return {'error': 'Invalid data'}


@router.get('/teachers', summary='Получить всех преподавателей')
async def get_teachers(session: AsyncSession = Depends(get_db)) -> list[STeacher]:
    return await TeacherDAO.find_all(session=session, order_by='short_name')

@router.get('/teachers/{id}', summary='Получить преподавателя по ID')
async def get_teacher_by_id(id: int, session: AsyncSession = Depends(get_db)) -> STeacher | None:
    return await TeacherDAO.find_one_or_none_by_id(session=session, id=id)
