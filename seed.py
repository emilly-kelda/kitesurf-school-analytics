"""
seed.py — Kitesurf School Analytics
Generates realistic watersports.db with 300 bookings

Run: python seed.py
"""
import sqlite3, random
from datetime import datetime, timedelta

# ── Realistic data pools ────────────────────────────────────────
STUDENTS = [
    "Lucas Silva", "Ana Costa", "Pedro Santos", "Maria Oliveira",
    "João Souza", "Carla Mendes", "Rafael Torres", "Beatriz Lima",
    "Diego Rocha", "Sofia Alves", "Thiago Ferreira", "Isabela Nunes",
    "Mateus Gomes", "Laura Pereira", "Felipe Barbosa", "Amanda Ramos",
]

INSTRUCTORS = [
    {"name": "Pedro",    "hourly_cost": 55},
    {"name": "Julia",    "hourly_cost": 50},
    {"name": "Fernanda", "hourly_cost": 45},
    {"name": "Marcos",   "hourly_cost": 40},
]

SPOTS = ["Cumbuco", "Jericoacoara", "Ilha do Guajiru", "Paracuru", "Taíba"]

STUDENT_LEVELS = ["beginner", "intermediate", "advanced"]

SPORTS_CONFIG = {
    "kitesurf": {
        "equipment": ["9m kite", "12m kite", "7m kite"],
        "base_price": (300, 480),
        # Northeast Brazil: peak wind Jun–Jan, low Apr–May
        "seasonal_boost": {6:1.2, 7:1.3, 8:1.25, 9:1.1, 10:1.1,
                           11:1.15, 12:1.2, 1:1.2, 2:1.1, 3:1.0,
                           4:0.85, 5:0.85},
    },
    "windsurf": {
        "equipment": ["windsurf board"],
        "base_price": (200, 380),
        "seasonal_boost": {6:1.15, 7:1.2, 8:1.2, 9:1.05, 10:1.05,
                           11:1.1, 12:1.15, 1:1.15, 2:1.1, 3:1.0,
                           4:0.9, 5:0.9},
    },
    "wingfoil": {
        "equipment": ["foil board"],
        "base_price": (250, 440),
        "seasonal_boost": {6:1.1, 7:1.2, 8:1.2, 9:1.1, 10:1.1,
                           11:1.1, 12:1.15, 1:1.2, 2:1.1, 3:1.0,
                           4:0.88, 5:0.88},
    },
}

DURATIONS   = [1, 1.5, 2, 2.5, 3]
STATUSES    = ["completed", "completed", "completed", "cancelled", "no_show"]

# ── Helpers ─────────────────────────────────────────────────────
def random_date():
    start = datetime(2025, 1, 1)
    end   = datetime(2026, 3, 1)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def seasonal_price(sport, date_str, level):
    cfg    = SPORTS_CONFIG[sport]
    month  = int(date_str.split("-")[1])
    boost  = cfg["seasonal_boost"].get(month, 1.0)
    bmin, bmax = cfg["base_price"]
    base   = random.randint(bmin, bmax)
    # Advanced students pay more (private coaching)
    level_mult = {"beginner": 1.0, "intermediate": 1.1, "advanced": 1.25}[level]
    return round(base * boost * level_mult / 10) * 10   # round to nearest 10

# ── Generate data ───────────────────────────────────────────────
rows = []
for _ in range(300):
    sport      = random.choices(list(SPORTS_CONFIG), weights=[0.4, 0.3, 0.3])[0]
    date       = random_date()
    instructor = random.choice(INSTRUCTORS)
    level      = random.choice(STUDENT_LEVELS)
    duration   = random.choice(DURATIONS)
    status     = random.choices(STATUSES, weights=[7,7,7,2,1])[0]
    price      = seasonal_price(sport, date, level) if status == "completed" else 0
    equipment  = random.choice(SPORTS_CONFIG[sport]["equipment"])
    cost       = round(duration * instructor["hourly_cost"], 2)
    profit     = round(price - cost, 2)

    rows.append((
        date,
        random.choice(STUDENTS),
        level,
        instructor["name"],
        random.choice(SPOTS),
        sport,
        equipment,
        price,
        duration,
        status,
        cost,
        profit,
        round(price / duration, 2) if duration and price else 0,
    ))

# ── Write to SQLite ─────────────────────────────────────────────
conn = sqlite3.connect("watersports.db")
conn.execute("DROP TABLE IF EXISTS bookings")
conn.execute("""
CREATE TABLE bookings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT,
    student_name    TEXT,
    student_level   TEXT,
    instructor      TEXT,
    spot            TEXT,
    sport           TEXT,
    equipment       TEXT,
    price           REAL,
    duration_hours  REAL,
    status          TEXT,
    cost            REAL,
    profit          REAL,
    revenue_per_hour REAL
)""")
conn.executemany("""
    INSERT INTO bookings
    (date,student_name,student_level,instructor,spot,sport,
     equipment,price,duration_hours,status,cost,profit,revenue_per_hour)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
conn.commit()
conn.close()
print(f"Done — {len(rows)} bookings written to watersports.db")