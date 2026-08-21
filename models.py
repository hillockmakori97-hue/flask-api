from sqlalchemy import ForeignKey
from sqlalchemy import String,Integer,Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
     pass

class User(Base):
    __tablename__='users'

    id : Mapped[int]=mapped_column(Integer,primary_key=True)
    full_name:Mapped[str]=mapped_column(String(100))
    email:Mapped[str]=mapped_column(String(100))
    password:Mapped[str]=mapped_column(String(100))

class Product(Base):
    __tablename__='products'

    id : Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    buying_price : Mapped[float]=mapped_column(Float)
    selling_price : Mapped[float]=mapped_column(Float)
