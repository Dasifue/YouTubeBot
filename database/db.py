from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Base, User, Message


def create_mysql_engine(user, password, host, port, database):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{int(port)}/{database}")
    return engine


def create_tables(engine):
    Base.metadata.create_all(engine, checkfirst=True)


def insert_user(engine, data):
    with Session(engine) as session:
        user = User(
            telegram_id=data["tg_id"],
            username=data["username"],
            full_name=data["full_name"],
        )
        session.add(user)
        try:
            session.commit()
            print(f"User {user} created") 
        except IntegrityError:
            pass


def insert_message(engine, data):
    with Session(engine) as session:
        message = Message(
            user_tg_id=data["user_tg_id"],
            text=data["text"],
        )
        session.add(message)
        try:
            session.commit()
            print(f"Message {message} created")
        except IntegrityError:
            pass


def change_message_text(engine, data):
    with Session(engine) as session:
        message = select(Message).where(Message.id==data["id"])
        message = session.scalars(message).one()
        message.text = data["text"]
        session.commit()
        print(f"Message {message} updated")


def get_user_messages(engine, user_tg_id):
    with Session(engine) as session:
        messages = select(Message).where(Message.user_tg_id==user_tg_id)
        messages = session.scalars(messages)
        return messages


def get_message(engine, message_id):
    with Session(engine) as session:
        message = select(Message).where(Message.id==message_id)
        message = session.scalars(message).one()
        return message
    