from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean,  and_, or_, desc, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    products = relationship("Product", back_populates="category")

Product.category = relationship("Category", back_populates="products")

engine = create_engine('sqlite:///db.test', echo=True)

Session = sessionmaker(bind=engine)
sync_session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def insert_categories(sync_session):
    with sync_session as session:
        session.add_all(
            [Category(name="Электроника", description="Гаджеты и устройства."),
             Category(name="Книги", description="Печатные книги и электронные книги."),
             Category(name="Одежда", description="Одежда для мужчин и женщин.")])
        session.commit()

def insert_products(sync_session):
    with sync_session as session:
        categories = session.query(Category).all()
        category_map = {category.name: category.id for category in categories}

        session.add_all(
            [Product(name="Смартфон", price=299.99, in_stock=True, category_id=category_map["Электроника"]),
             Product(name="Ноутбук", price=499.99, in_stock=True, category_id=category_map["Электроника"]),
             Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=category_map["Книги"]),
             Product(name="Джинсы", price=40.50, in_stock=True, category_id=category_map["Одежда"]),
             Product(name="Футболка", price=20.00, in_stock=True, category_id=category_map["Одежда"])])
        session.commit()

# Вставка категорий
print('Вставка категорий')
insert_categories(sync_session)

# Вставка продуктов
print('Вставка продуктов')
insert_products(sync_session)


# Извлечение категорий и связанных продуктов
def fetch_categories_and_products(session):
    with session as session:
        categories = session.query(Category).all()
        for category in categories:
            print(f"Категория: {category.name} ({category.description})")
            # Извлечение связанных продуктов для каждой категории
            products = session.query(Product).filter_by(category_id=category.id).all()
            for product in products:
                print(f"  Продукт: {product.name}, Цена: {product.price}")

print('Извлечение категорий и связанных продуктов')
fetch_categories_and_products(sync_session)


def update_smartphone_price(session):
    with session as session:
        # Найти первый продукт с названием "Смартфон"
        smartphone = session.query(Product).filter(Product.name == "Смартфон").first()
        if smartphone:
            # Заменить цену на 349.99
            smartphone.price = 349.99
            # Сохранить изменения
            session.commit()
            print(f"Цена продукта '{smartphone.name}' была обновлена до {smartphone.price}")
        else:
            print("Продукт с названием 'Смартфон' не найден")

# Обновление цены смартфона
print("Обновление цены смартфона")
update_smartphone_price(sync_session)


def aggregate_products_by_category(session):
    with session as session:
        # Выполнение агрегации и группировки
        results = session.query(Category.name, func.count(Product.id).label('product_count')).\
                          join(Product).\
                          group_by(Category.name).\
                          all()

        # Вывод результатов
        for category_name, product_count in results:
            print(f"Категория: {category_name}, Количество продуктов: {product_count}")

def filter_categories_with_more_than_one_product(session):
    with session as session:
        # Выполнение агрегации, группировки и фильтрации
        results = session.query(Category.name, func.count(Product.id).label('product_count')).\
                          join(Product).\
                          group_by(Category.name).\
                          having(func.count(Product.id) > 1).\
                          all()

        # Вывод результатов
        for category_name, product_count in results:
            print(f"Категория: {category_name}, Количество продуктов: {product_count}")

# Агрегация и группировка
print("Агрегация и группировка")
aggregate_products_by_category(sync_session)

# Группировка с фильтрацией
print("Группировка с фильтрацией")
filter_categories_with_more_than_one_product(sync_session)