# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# 创建一个SQLite数据库引擎，指定数据库文件名为comic.db
engine = create_engine('sqlite:///comic.db')
Base = declarative_base()


# class Comic(Base):
#     __tablename__ = 'comic'  # 表名
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     url = Column(String(150), unique=True)
#     cover_url = Column(String(150), unique=True)
#
#
# class Chapter(Base):
#     __tablename__ = 'chapter'  # 表名
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     url = Column(String(150), unique=True)
#     Comic_name = Column(String(150))


class Pic(Base):
    __tablename__ = 'pic'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    target_url = Column(String(150))
    url = Column(String(500))
    Chapter_title = Column(String(150))
    Chapter_url = Column(String(150))
    Comic_name = Column(String(150))
    Comic_cover = Column(String(150))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    name = Column(String(16), unique=True)
    email = Column(String(32), unique=True)
    password = Column(String(16))

    def __repr__(self):
        return "User: %s %s %s %s" % (self.id, self.name, self.email, self.password)


class user_history(Base):
    __tablename__ = "history"
    id = Column(Integer(), primary_key=True)
    name = Column(String(16))
    comic_name = Column(String(50))
    title = Column(String(50))
    createTime = Column(DATETIME(), default=datetime.now(), nullable=False)

    def __repr__(self):
        return "User: %s %s %s %s" % (self.id, self.name, self.comic_name, self.title)


def session_0():
    Session = sessionmaker(bind=engine)  # 构建session对象
    session = Session()
    return session


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)  # 将模型映射到数据库中
