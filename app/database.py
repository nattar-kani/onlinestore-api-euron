from sqlalchemy import create_engine, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = "mssql+pyodbc://DESKTOP-D3BLDPV/onlinestore_euron?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()