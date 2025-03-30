from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.feedback.dao import FeedbackDAO
from app.feedback.rb import RBFeedback
from app.feedback.schemas import SFeedback, SFeedbackCreate

router = APIRouter(prefix='/feedbacks', tags=['Обратная связь'])

@router.get('', summary='Получить все отчеты', status_code=200)
async def get_feedbacks(request_body: RBFeedback = Depends(), session: AsyncSession = Depends(get_db)) -> list[SFeedback]:
    return await FeedbackDAO.find_all(session=session, **request_body.to_dict())

@router.post('', summary='Создать отчет', status_code=201)
async def create_feedback(feedback: SFeedbackCreate, session: AsyncSession = Depends(get_db)) -> SFeedback:
    return await FeedbackDAO.add(session=session, **feedback.model_dump())

@router.get('/{id}', summary='Получить отчет по ID', status_code=200)
async def get_feedback(id: int, session: AsyncSession = Depends(get_db)) -> SFeedback | None:
    return await FeedbackDAO.find_one_or_none_by_id(session=session, id=id)
