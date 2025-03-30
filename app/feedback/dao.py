from app.dao.base import BaseDAO
from app.feedback.models import Feedback


class FeedbackDAO(BaseDAO):
    model = Feedback
