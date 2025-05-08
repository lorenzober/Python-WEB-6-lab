from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})

users_to_add = [
    ('Admin', 'Admin', 'password', 1, 'admin@gmail.com', 123456789),
    ('Alice', 'Smith', 'alicepass', 0, 'alice@example.com', 111222333),
    ('Bob', 'Brown', 'bobpass', 0, 'bob@example.com', 444555666)
]

with engine.begin() as conn:
    existing_emails = {
        row[0]
        for row in conn.execute(text('SELECT emailUser FROM Users')).fetchall()
    }

    for name, surname, pwd, is_admin, email, phone in users_to_add:
        if email in existing_emails:
            print(f"⛔️ Email already exists: {email} — skipping.")
            continue

        conn.execute(text("""
            INSERT INTO Users (nameUser, surnameUser, passwordUser, is_admin, emailUser, numberUser)
            VALUES (:name, :surname, :pwd, :admin, :email, :phone)
        """), {
            "name": name,
            "surname": surname,
            "pwd": pwd,
            "admin": is_admin,
            "email": email,
            "phone": phone
        })

    print("✅ Done: all new users added (duplicates skipped)")
