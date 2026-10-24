"""
skillswap/
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py          # Підключення до бази даних та залежність get_db
│   │   └── models.py      # SQLAlchemy моделі (User, Skill, Exchange, Review)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py       # API ендпоінти для користувачів
│   │   ├── skills.py      # API ендпоінти для навичок
│   │   ├── exchanges.py   # API ендпоінти для обмінів
│   │   └── reviews.py     # API ендпоінти для відгуків
│   └── schemas.py         # Pydantic схеми для валідації даних
├── .env                   # Змінні середовища
├── requirements.txt       # Залежності проєкту
└── main.py                # Головна точка входу FastAPI (підключення роутерів через APIRouter)"""