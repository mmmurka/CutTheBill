from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from constrains import DATABASE_SYNC_URL
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

# 📦 Очистка та створення таблиць
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# 👤 Створюємо користувачів
user1 = User(telegram_id=1001, username="alice")
user2 = User(telegram_id=1002, username="bob")

# 🎵 Створюємо сервіси
service_yt = Service(name="YouTube", subscription_price=60.0, user_price=10.0)
service_spotify = Service(name="Spotify", subscription_price=50.0, user_price=8.0)

# 🔗 Зв'язки user-service
link1 = LinkedService(user=user1, service=service_yt)
link2 = LinkedService(user=user2, service=service_yt)

# 💰 Платежі
payment1 = Payment(
    linked_service=link1,
    last_payment=datetime.now() - timedelta(days=30),
    next_payment=datetime.now()
)

# 👥 Група
group = Group(
    group_name="YouTube Premium Family",
    service=service_yt,
    max_slots=6,
    free_slots=4,
    admin_email="admin@example.com"
)

# 👤 Додавання користувачів до групи
group_user1 = GroupUser(group=group, user=user1)
group_user2 = GroupUser(group=group, user=user2)

# 📥 Додавання до сесії
session.add_all([
    user1, user2,
    service_yt, service_spotify,
    link1, link2,
    payment1,
    group,
    group_user1, group_user2
])

session.commit()

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
