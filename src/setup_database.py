import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('rhythm_restore.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    sleep_time TEXT,
    wake_time TEXT,
    meals_skipped TEXT,
    mood TEXT,
    work_stress TEXT,
    traffic TEXT,
    stress_level TEXT,
    screen_time TEXT,
    relaxation TEXT,
    exercise TEXT,
    caffeine TEXT,
    conflict TEXT,
    diet_suggestion TEXT,
    workout_suggestion TEXT,
    sleep_habit_suggestion TEXT,
    stress_buster_suggestion TEXT
)
''')

# Commit and close
conn.commit()
conn.close()

print("✅ Database and table created successfully!")
