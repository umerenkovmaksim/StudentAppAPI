
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.students.models import Group


@pytest.mark.asyncio
async def test_create_group_with_valid_data(client: TestClient, test_db: AsyncSession):
    group = client.post('/groups', json={'short_name': 'Группа 1', 'degree': 1, 'institute': 'Институт 1'})

    cursor = await test_db.execute(select(Group))
    objects = cursor.fetchall()

    assert group.status_code == HTTPStatus.CREATED
    assert len(objects) == 1
