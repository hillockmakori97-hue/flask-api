from sqlalchemy import ForeignKey
from sqlalchemy import String,Integer,Float,Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import date


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




class Sale(Base):
    __tablename__='sales'

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey('users.id'))
    date_sold:Mapped[date]=mapped_column(Date)





class Payment(Base):
    __tablename__='payments'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    sale_id:Mapped[int]=mapped_column(Integer,ForeignKey('sales.id'))
    date_paid:Mapped[date]=mapped_column(Date)




class Purchase(Base):
    __tablename__='purchases'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    product_id:Mapped[int]=mapped_column(Integer,ForeignKey('products.id'))
    purchase_price :  Mapped[Float] = mapped_column(Float)
    date_purchased:Mapped[date]=mapped_column(Date)




class Sale_detail(Base):
    __tablename__='sales_details'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    product_id:Mapped[int]=mapped_column(Integer,ForeignKey('products.id'))
    sale_id:Mapped[int]=mapped_column(Integer,ForeignKey('sales.id'))
    quantity:Mapped[float]=mapped_column(Float)
    amount:Mapped[int]=mapped_column(Integer)
