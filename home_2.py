from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Создание экземпляра движка для базы данных в памяти
engine = create_engine('sqlite:///:memory:', echo=True)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Создание базового класса для декларативных классов
Base = declarative_base()

# Определение модели продукта
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    # Определение отношения к категории
    category = relationship('Category', back_populates='products')

# Определение модели категории
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    # Обратное отношение к продуктам
    products = relationship('Product', order_by=Product.id, back_populates='category')

# Создание всех таблиц в базе данных
Base.metadata.create_all(engine)

# Пример добавления данных
new_category = Category(name='Electronics', description='Electronic items')
new_product = Product(name='Smartphone', price=699.99, in_stock=True, category=new_category)

session.add(new_category)
session.add(new_product)

# Сохранение изменений
session.commit()

# Закрытие сессии
session.close()