import enum
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String, Enum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class PaymentStatus(enum.Enum):
    WAITING = "waiting"
    PAID = "paid"
    EXPIRED = "expired"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=False)
    username = Column(String, unique=True, nullable=True)

    linked_services = relationship("LinkedService", back_populates="user", cascade="all, delete")
    groups_assoc = relationship("GroupUser", back_populates="user", cascade="all, delete")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    subscription_price = Column(Float, nullable=False)
    user_price = Column(Float, nullable=False)

    linked_services = relationship("LinkedService", back_populates="service", cascade="all, delete")


class LinkedService(Base):
    __tablename__ = "linked_services"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    service_id = Column(ForeignKey("services.id"), nullable=False)

    user = relationship("User", back_populates="linked_services")
    service = relationship("Service", back_populates="linked_services")

    payments = relationship("Payment", back_populates="linked_service", cascade="all, delete")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    group_name = Column(String, unique=False)
    service_id = Column(ForeignKey("services.id"), nullable=False)
    max_slots = Column(Integer, nullable=False)
    free_slots = Column(Integer, nullable=False)
    admin_email = Column(String)

    service = relationship("Service", backref="groups")
    users_assoc = relationship("GroupUser", back_populates="group", cascade="all, delete")

class GroupUser(Base):
    __tablename__ = "group_users"

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey("groups.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    email = Column(String, nullable=False)

    group = relationship("Group", back_populates="users_assoc")
    user = relationship("User", back_populates="groups_assoc")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    linked_service_id = Column(ForeignKey("linked_services.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus, default=PaymentStatus.WAITING, nullable=False))
    payment_code = Column(String, unique=True, nullable=True)

    linked_service = relationship("LinkedService", back_populates="payments")
    payment_logs = relationship("PaymentLog", back_populates="payment")

class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id = Column(Integer, primary_key=True)
    payment_id = Column(ForeignKey("payments.id"), nullable=False)
    amount = Column(Float, nullable=False)
    paid_at = Column(DateTime)
    payment = relationship("Payment", back_populates="payment_logs")

