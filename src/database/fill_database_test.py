from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from constants import DATABASE_SYNC_URL
from src.database.models import (
    Base,
    User,
    Service,
    LinkedService,
    Payment,
    Group,
    GroupUser,
)

DATABASE_URL = DATABASE_SYNC_URL
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# ✅ Вивід для перевірки
print("\n=== USERS ===")
for u in session.query(User).all():
    print(f"{u.username} → {[ls.service.name for ls in u.linked_services]}")

print("\n=== GROUPS ===")
for g in session.query(Group).all():
    print(f"{g.group_name} ({g.service.name}) → {[gu.user.username for gu in g.users_assoc]}")

print("\n=== PAYMENTS ===")
for p in session.query(Payment).all():
    print(f"{p.linked_service.user.username} → Last: {p.last_payment}, Next: {p.next_payment}")
