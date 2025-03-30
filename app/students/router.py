from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.students.dao import GroupDAO, StudentDAO
from app.students.rb import RBGroup, RBStudent
from app.students.schemas import (
    SGroup,
    SGroupAdd,
    SGroupUpdate,
    SStudent,
    SStudentAdd,
    SStudentUpdate,
)

router = APIRouter(prefix='', tags=['Студенты'])

@router.get('/students', summary='Получить всех студентов', status_code=200)
async def get_students(request_body: RBStudent = Depends(), session: AsyncSession = Depends(get_db)) -> list[SStudent]:
    return await StudentDAO.find_all(session=session, **request_body.to_dict())

@router.post('/students', summary='Добавить студента', status_code=201)
async def add_student(student: SStudentAdd, session: AsyncSession = Depends(get_db)) -> SStudent:
    return await StudentDAO.add(session=session, **student.model_dump())

@router.patch('/students/{id}', summary='Изменить данные студента по ID', status_code=204)
async def update_student_by_id(id: int, data: SStudentUpdate, session: AsyncSession = Depends(get_db)):
    await StudentDAO.update(session=session, filter_by={'id': id}, **data.model_dump(exclude_unset=True))

@router.get('/students/{id}', summary='Получить данные студента по ID', status_code=200)
async def get_student_by_id(id: int, session: AsyncSession = Depends(get_db)) -> SStudent:
    student = await StudentDAO.find_one_or_none_by_id(id=id, session=session)
    if student:
        return student
    raise HTTPException(status_code=404, detail='invalid id')

@router.delete('/students/{id}', summary='Удалить данные студента по ID')
async def delete_student_by_id(id: int, session: AsyncSession = Depends(get_db)):
    rows = await StudentDAO.delete(session=session, id=id)
    if not rows:
        raise HTTPException(status_code=404, detail='this student is not found')

@router.get('/groups', summary='Получить все группы')
async def get_groups(request_body: RBGroup = Depends(), session: AsyncSession = Depends(get_db)) -> list[SGroup]:
    return await GroupDAO.find_all(session=session, **request_body.to_dict())

@router.post('/groups', summary='Добавить группу', status_code=201)
async def add_groups(group: SGroupAdd | list[SGroupAdd], session: AsyncSession = Depends(get_db)) -> dict:
    if isinstance(group, list):
        check = await GroupDAO.add_many(session=session, items=(item.model_dump() for item in group))
        if check:
            return {'message': f'{len(check) if isinstance(check, list) else 1} group(s) was added'}
        return {'error': 'invalid data'}
    check = await GroupDAO.add(session=session, **group.model_dump())
    if check:
        return SGroup(**check.__dict__).model_dump()
    return {'error': 'invalid data'}

@router.get('/groups/{id}', summary='Получить группу по ID')
async def get_group(id: int, session: AsyncSession = Depends(get_db)) -> SGroup:
    return await GroupDAO.find_one_or_none_by_id(session=session, id=id)

@router.patch('/groups/{id}', summary='Обновить данные группы по ID', status_code=204)
async def update_group(id: int, group: SGroupUpdate, session: AsyncSession = Depends(get_db)):
    check = await GroupDAO.update(session=session, filter_by={'id': id}, **group.model_dump(exclude_unset=True))
    if not check:
        raise HTTPException(status_code=422, detail='invalid data')

@router.delete('/groups/{id}', summary='Удалить группу по ID')
async def delete_group(id: int, session: AsyncSession = Depends(get_db)) -> dict:
    count = await GroupDAO.delete(session=session, id=id)
    if count > 0:
        return JSONResponse(content={'message': f'{count} group(s) was deleted'}, status_code=200)
    raise HTTPException(status_code=404, detail='this group is not found')

@router.get('/institutes', summary='Получить все институты')
async def get_institutes(session: AsyncSession = Depends(get_db)) -> list[str]:
    return await GroupDAO.get_institutes(session=session)
