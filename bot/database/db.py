from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from .models import Base, User, Message, Admin, MessageStatus


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
        message = select(Message).where(Message.id==data["message"])
        message = session.scalars(message).one()
        message.text = data["text"]
        session.commit()
        print(f"Message {message} updated")


def get_user_messages(engine, user_tg_id):
    with Session(engine) as session:
        messages = select(Message).where(Message.user_tg_id==user_tg_id)
        messages = session.scalars(messages).fetchall()
    return messages


def get_message(engine, message_id):
    with Session(engine) as session:
        message = select(Message).where(Message.id==message_id)
        message = session.scalars(message).one()
    return message


def get_message_author(engine, message_id):
    with Session(engine) as session:
        message=get_message(engine, message_id=message_id)
        author_tg_id=message.user_tg_id
    return author_tg_id
    

def get_messages_in_queue(engine):
    with Session(engine) as session:
        messages = select(Message).where(Message.status==MessageStatus.InQueue)
        messages = session.scalars(messages).all()
    return messages


def delete_message(engine, message_id):
    with Session(engine) as session:
        message = select(Message).where(Message.id==message_id)
        message = session.scalar(message)
        session.delete(message)
        session.commit()
    

def check_admin_exists(engine, user_tg_id):
    with Session(engine) as session:
        admin = select(Admin).where(Admin.id==user_tg_id)
        try:
            session.scalars(admin).one()
        except NoResultFound:
            return False
        else:
            return True

            


def insert_admin(engine, data):
    with Session(engine) as session:
        admin = Admin(
            id=data["user_tg_id"],
            email=data["email"]
        )
        session.add(admin)
        session.commit()


def change_message_status(engine, message_id, status):
    with Session(engine) as session:
        message = select(Message).where(Message.id==message_id)
        message = session.scalars(message).one()
        message.status = status
        session.commit()