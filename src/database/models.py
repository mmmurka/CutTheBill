
from sqlalchemy import Column, Integer, Table, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String, unique=True, nullable=True)

    linked_services = relationship("LinkedService", back_populates="user", cascade="all, delete")
    groups_assoc = relationship("GroupUser", back_populates="user", cascade="all, delete")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    subscription_price = Column(Float)
    user_price = Column(Float)

    linked_services = relationship("LinkedService", back_populates="service", cascade="all, delete")


class LinkedService(Base):
    __tablename__ = "linked_services"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    service_id = Column(ForeignKey("services.id"))

    user = relationship("User", back_populates="linked_services")
    service = relationship("Service", back_populates="linked_services")

    payments = relationship("Payment", back_populates="linked_service", cascade="all, delete")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    linked_service_id = Column(ForeignKey("linked_services.id"))

    last_payment = Column(DateTime)
    next_payment = Column(DateTime)

    linked_service = relationship("LinkedService", back_populates="payments")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    group_name = Column(String, unique=True)
    service_id = Column(ForeignKey("services.id"), nullable=False)
    max_slots = Column(Integer, nullable=False)
    free_slots = Column(Integer, nullable=False)
    admin_email = Column(String)

    service = relationship("Service", backref="groups")
    users_assoc = relationship("GroupUser", back_populates="group", cascade="all, delete")

class GroupUser(Base):
    __tablename__ = "group_users"

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey("groups.id"))
    user_id = Column(ForeignKey("users.id"))

    group = relationship("Group", back_populates="users_assoc")
    user = relationship("User", back_populates="groups_assoc")

