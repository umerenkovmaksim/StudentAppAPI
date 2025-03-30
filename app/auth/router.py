import random
import string

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import GroupLeadershipDAO, StudentConfirmationDAO
from app.auth.schemas import (
    SGroupLeadershipCheck,
    SStudentConfirmationCheck,
    SStudentConfirmationCreate,
)
from app.database import get_db
from app.students.dao import StudentDAO
from app.students.schemas import SStudent

router = APIRouter(prefix='/auth', tags=['Авторизация'])

@router.post('/students/create_confirmation', status_code=201)
async def create_confirmation(confirmation: SStudentConfirmationCreate, session: AsyncSession = Depends(get_db)):
    check = await StudentConfirmationDAO.find_one_or_none(session, email=confirmation.email)
    if check:
        if check.attempts > 0:
            await StudentConfirmationDAO.delete(session, id=check.id)
        else:
            raise HTTPException(status_code=403, detail={'error': 'not enough attempts'})
    symbols = string.ascii_letters + string.digits
    code = ''.join(random.choices(symbols, k=6))
    confirmation_instance = await StudentConfirmationDAO.add(session, code=code, **confirmation.model_dump())
    if confirmation_instance:
        return {'message': 'confirmation code created'}
    raise HTTPException(status_code=404, detail={'error': 'not found'})

@router.post('/students/confirm_create', status_code=201)
async def create_student_confirm(confirmation: SStudentConfirmationCheck, session: AsyncSession = Depends(get_db)) -> SStudent:
    confirm = await StudentConfirmationDAO.find_one_or_none(session, **confirmation.model_dump())
    if confirm:
        student_data = {
            'student_id': confirm.student_id,
            'telegram_id': confirm.telegram_id,
            'email': confirm.email,
            'first_name': confirm.first_name,
            'last_name': confirm.last_name,
        }
        return await StudentDAO.add(session, **student_data)
    is_invalid_code = await StudentConfirmationDAO.find_one_or_none(session, email=confirmation.email)
    if is_invalid_code:
        attempts = is_invalid_code.attempts - 1
        if attempts == 0:
            await StudentConfirmationDAO.update(session, filter_by={'id': is_invalid_code.id}, attempts=attempts)
            raise HTTPException(status_code=403, detail={'error': 'not enough attempts'})
        if attempts > 0:
            await StudentConfirmationDAO.update(session, filter_by={'id': is_invalid_code.id}, attempts=attempts)
            raise HTTPException(status_code=400, detail={'error': 'invalid code', 'attempts': attempts})
        raise HTTPException(status_code=403, detail={'error': 'not enough attempts'})
    raise HTTPException(status_code=404, detail={'error': 'not found'})

@router.post('/students/check_confirmation')
async def check_confirmation(confirmation: SStudentConfirmationCheck, session: AsyncSession = Depends(get_db)):
    return await StudentConfirmationDAO.find_one_or_none(session=session, **confirmation.model_dump())

@router.get('/students/check_group_leadership')
async def check_group_leadership(leadership: SGroupLeadershipCheck, session: AsyncSession = Depends(get_db)):
    check = await GroupLeadershipDAO.find_one_or_none(session=session, **leadership.model_dump())
    if check:
        return JSONResponse(status_code=200, content={'message': 'ok'})
    raise HTTPException(status_code=404, detail={'error': 'not found'})
