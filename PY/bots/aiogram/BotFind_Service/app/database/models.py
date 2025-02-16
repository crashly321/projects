from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50))
    number: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    rating: Mapped[str] = mapped_column(String(50))
    num_rating: Mapped[int] = mapped_column()

class User_rating(Base):
    __tablename__ = 'users_rating'

    id: Mapped[int] = mapped_column(primary_key=True)



class Tech_service(Base):
    __tablename__ = 'Tech_services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    rating: Mapped[str] = mapped_column(String(50))
    num_rating: Mapped[int] = mapped_column()




async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)