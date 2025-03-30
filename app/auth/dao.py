from app.dao.base import BaseDAO
from app.students.models import GroupLeadership, StudentConfirmation


class StudentConfirmationDAO(BaseDAO):
    model = StudentConfirmation

class GroupLeadershipDAO(BaseDAO):
    model = GroupLeadership
