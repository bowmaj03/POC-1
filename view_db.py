import sqlite3

db_path = "risk_register.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM risk_register;")
rows = cursor.fetchall()

print("\n=== Risk Register ===")
for row in rows:
    print(f"ID: {row[0]}, Risk: {row[1]}, Created: {row[2]}")

conn.close()
print("\nDone!")
