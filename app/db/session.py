from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# engine = create_engine(settings.DB_URI, pool_pre_ping=True)
engine = create_engine(settings.DB_URI, pool_size=40, max_overflow=0, pool_timeout=5)  #, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# from contextlib import contextmanager

# import sqlalchemy as sa
# from sqlalchemy.orm import sessionmaker

# main_engine = sa.create_engine(
#     settings.DB_URI,
#     echo=True,
# )

# DBSession = sessionmaker(
#     # binds={
#     #     Base: main_engine,
#     # },
#     bind=main_engine,
#     expire_on_commit=False,
# )

# @contextmanager
# def session_scope():
#     """Provides a transactional scope around a series of operations."""
#     session = DBSession()
#     try:
#         yield session
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         raise e
#     finally:
#         session.close()

# if __name__ == '__main__':
#     with session_scope() as s:
#         # 




