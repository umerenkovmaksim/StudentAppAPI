from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.students.models import StudentConfirmation
from app.students.schemas import SStudent


@pytest.mark.asyncio
async def test_create_confirmation_code_with_valid_data(client: TestClient, test_db: AsyncSession):
    response = client.post('/auth/students/create_confirmation', json={'email': 'test@gmail.com', 'telegram_id': 123})
    cursor = await test_db.execute(select(StudentConfirmation))
    objects = cursor.fetchall()

    assert response.status_code == HTTPStatus.CREATED
    assert len(objects) == 1

@pytest.mark.asyncio
async def test_create_confirmation_code_with_invalid_data(client: TestClient, test_db: AsyncSession):
    response = client.post('/auth/students/create_confirmation', json={'email': 'testgmail.com', 'telegram_id': 'qwqwc'})
    cursor = await test_db.execute(select(StudentConfirmation))
    objects = cursor.fetchall()

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(objects) == 0


@pytest.mark.asyncio
async def test_create_user_with_valid_confirmation(client: TestClient, test_db: AsyncSession):
    user = {'id': 1, 'email': 'test@gmail.com', 'telegram_id': 123}
    response = client.post('/auth/students/create_confirmation', json=user)
    cursor = await test_db.execute(select(StudentConfirmation))
    code = cursor.scalar_one_or_none().code
    response = client.post('/auth/students/confirm_create', json={'email': 'test@gmail.com', 'code': code})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == SStudent(**user).model_dump()
