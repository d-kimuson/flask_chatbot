from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_path = "chatbot.db"
Base = declarative_base()


class DBController:
    def __init__(self):
        self.url = f"sqlite:///{db_path}"
        self.engine = create_engine(self.url, echo=False)
        self.Base = Base
        self.Base.metadata.create_all(self.engine)
        self.Sess_maker = sessionmaker(bind=self.engine)
        self.tables = [
            "users",
        ]
        self.sess = self.Sess_maker()

    def add_user(self, name=None, mail=None, password=None):
        if mail is not None and password is not None:
            # 同じメールアドレス持ちが存在しない
            if not self.is_existed_user(mail):
                if name is None:
                    name = "名無し"
                user = User(name=name, mail=mail, password=password)
                self.sess.add(user)
                self.sess.commit()
                return True  # 成功
            else:
                return False  # 既に登録済み
        else:
            return False  # 入力エラー

    def update_user(self, mail, **kwargs):
        """
        mail -> アップデートするユーザーのアドレス
        kwargs -> キーワード引数で, 更新したいパラメータを.
        """
        user = self.sess.query(User).filter_by(mail=mail).one()
        if "name" in kwargs.keys():
            user.name = kwargs["name"]
        if "mail" in kwargs.keys():
            user.mail = kwargs["mail"]
        if "password" in kwargs.keys():
            user.password = kwargs["password"]
        self.sess.add(user)
        self.sess.commit()

    def delete_user(self, mail):
        user = self.session.query(User).filter_by(mail=mail).one()
        self.session.delete(user)
        self.session.commit()

    def read_users(self):
        return self.session.query(User).all()

    def is_existed_user(self, mail):
        response = self.sess.query(User).filter_by(mail=mail).first()
        if response is None:
            return False
        else:
            return True
        self.sess.commit()

    def get_value(self, mail, key):
        user = self.sess.query(User).filter_by(mail=mail).one()
        value = None
        if key == "id":
            value = user.id
        elif key == "name":
            value = user.name
        elif key == "mail":
            value = user.mail
        elif key == "password" or key == "passwd":
            value = user.password
        return value

    def auth(self, mail, password):
        if self.is_existed_user(mail):
            if password == self.get_value(mail, key="password"):
                return True
        return False


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    mail = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(id='%s', name='%s', mail='%s', password='%s')>" % (
            self.id,
            self.name,
            self.mail,
            self.password
            )
