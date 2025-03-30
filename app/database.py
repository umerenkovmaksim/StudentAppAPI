from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
int_uniq = Annotated[int, mapped_column(unique=True)]
int_null_true = Annotated[int, mapped_column(nullable=True)]
str_uniq = Annotated[str, mapped_column(unique=True)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

async def get_db():
    async with async_session_maker() as session:
        yield session
        await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=datetime.now)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return f'{cls.__name__.lower()}s'
