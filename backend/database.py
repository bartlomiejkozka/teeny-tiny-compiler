from typing import List 
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id:         Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:       Mapped[str] = mapped_column(String(30))
    login:       Mapped[str] = mapped_column(String(30))
    password:   Mapped[str] = mapped_column(String(50))

    scripts: Mapped[List['Script']] = relationship(back_populates='user')
    session_tokens: Mapped[List['SessionToken']] = relationship(back_populates='user')

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, login={self.login!r})"


class Script(Base):
    __tablename__ = 'scripts'

    id:             Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pesudo_code:    Mapped[str] = mapped_column(String(10000))
    user_id:        Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='scripts')

    def __repr__(self):
        return f"Script(id={self.id!r}, pesudo_code={self.pesudo_code!r}, user_id={self.user_id!r})"
    

class SessionToken(Base):
    __tablename__ = 'session_tokens'

    token:      Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id:    Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='session_tokens')

    def __repr__(self):
        return f"SessionToken(id={self.id!r}, token={self.token!r}, user_id={self.user_id!r})"



class Database:
    def __init__(self, user, password, host, port, database):
        self.database_url = "mysql+pymysql://" + user + ":" + password + "@" + host + ":" + port + "/" + database
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
