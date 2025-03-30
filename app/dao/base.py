import typing

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class BaseDAO:
    model: type = None
    order_by: typing.Any = None

    @classmethod
    async def find_all(
        cls, session: AsyncSession, order_by: typing.Any = None, **filter_by: typing.Any,
    ) -> list[model]:
        query = select(cls.model).filter_by(**filter_by)
        if order_by:
            query = query.order_by(getattr(cls.model, order_by))
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, id: int) -> model | None:
        query = select(cls.model).filter_by(id=id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(
        cls, session: AsyncSession, **filter_by: typing.Any,
    ) -> model | None:
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, **values: typing.Any) -> model:
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(
        cls, session: AsyncSession, items: list[dict[str, typing.Any]],
    ) -> list[model]:
        objects = []
        for item in items:
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
    async def update(
        cls, session: AsyncSession, filter_by: dict[str, typing.Any], **values: typing.Any,
    ) -> int:
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
            .values(**values)
            .execution_options(synchronize_session='fetch')
        )
        result = await session.execute(query)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount

    @classmethod
    async def delete(
        cls, session: AsyncSession, delete_all: bool = False, **filter_by: typing.Any,
    ) -> int:
        if not delete_all and not filter_by:
            raise ValueError('No objects to delete')

        query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount

    @classmethod
    async def get_or_create(
        cls, session: AsyncSession, **values: typing.Any,
    ) -> tuple[model, bool]:
        try:
            instance = await cls.find_one_or_none(session=session, **values)
            if instance:
                return instance, False
            instance = await cls.add(session=session, **values)
            return instance, True
        except IntegrityError:
            return await cls.find_one_or_none(session=session, **values), False
