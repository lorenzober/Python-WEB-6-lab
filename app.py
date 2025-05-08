# File: app.py
from flask import Flask, request, jsonify, render_template, redirect, make_response, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, User, Book, Author, Category, History
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# DB config
database_url = 'sqlite:///sql_app.db'
engine = create_engine(database_url, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db, email, password):
    user = db.query(User).filter(User.emailUser == email).first()
    if user and user.check_password(password):
        return user
    return None

@app.route('/')
def root():
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    db = next(get_db())
    data = request.json
    user = authenticate_user(db, data.get("emailUser"), data.get("passwordUser"))
    if user:
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie("email", data.get("emailUser"))
        response.set_cookie("password", data.get("passwordUser"))
        return response
    return jsonify({"detail": "Login failed"}), 401

@app.route('/registration', methods=['GET'])
def registration_page():
    return render_template('registration.html')

@app.route('/registration', methods=['POST'])
def register():
    db = next(get_db())
    data = request.json
    try:
        user = User(**data)
        db.add(user)
        db.commit()
        return jsonify({"message": "Registered successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"detail": "Registration failed"}), 400

@app.route('/book-list')
def book_list():
    db = next(get_db())
    email = request.cookies.get("email")
    password = request.cookies.get("password")
    user = authenticate_user(db, email, password)
    if user:
        books = db.query(Book).all()
        if user.is_admin:
            return render_template('book-list-roles/admin-book-list.html', books=books, username=email)
        else:
            rents = db.query(History).filter(History.user_id == user.id, History.isReturned == False).all()
            rent_ids = [r.books_id for r in rents]
            return render_template('book-list-roles/user-book-list.html', books=books, username=email, rents_book_id=rent_ids)
    return redirect('/login')

@app.route('/book/<int:book_id>')
def get_book(book_id):
    db = next(get_db())
    book = db.query(Book).get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify({"id": book.id, "nameBook": book.nameBook, "yearBook": book.yearBook})

@app.route('/book', methods=['POST'])
def add_book():
    db = next(get_db())
    data = request.json
    user = authenticate_user(db, request.cookies.get("email"), request.cookies.get("password"))
    if not user or not user.is_admin:
        return jsonify({"detail": "Unauthorized"}), 401
    book = Book(**data)
    db.add(book)
    db.commit()
    return jsonify({"id": book.id})

@app.route('/book', methods=['PUT'])
def update_book():
    db = next(get_db())
    data = request.json
    user = authenticate_user(db, request.cookies.get("email"), request.cookies.get("password"))
    if not user or not user.is_admin:
        return jsonify({"detail": "Unauthorized"}), 401
    book = db.query(Book).get(data["id"])
    if not book:
        return jsonify({"message": "Book not found"}), 404
    for key, value in data.items():
        setattr(book, key, value)
    db.commit()
    return jsonify({"id": book.id})

@app.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    db = next(get_db())
    user = authenticate_user(db, request.cookies.get("email"), request.cookies.get("password"))
    if not user or not user.is_admin:
        return jsonify({"detail": "Unauthorized"}), 401
    book = db.query(Book).get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    db.delete(book)
    db.commit()
    return jsonify({"message": "Book deleted"})

@app.route('/book/<int:book_id>/rent', methods=['POST'])
def rent_book(book_id):
    db = next(get_db())
    now = datetime.now()
    user = authenticate_user(db, request.cookies.get("email"), request.cookies.get("password"))
    if not user:
        return jsonify({"detail": "Authentication failed"}), 401
    rent = db.query(History).filter_by(user_id=user.id, books_id=book_id, isReturned=False).first()
    book = db.query(Book).get(book_id)
    if rent:
        rent.isReturned = True
        rent.dateReturn = now
        book.availableBook += 1
    else:
        new_rent = History(user_id=user.id, books_id=book_id, dateLoan=now, isReturned=False)
        db.add(new_rent)
        book.availableBook -= 1
    db.commit()
    return jsonify({"message": "Rent updated"})

@app.route('/rents-list')
def rents_list():
    db = next(get_db())
    user = authenticate_user(db, request.cookies.get("email"), request.cookies.get("password"))
    if not user or not user.is_admin:
        return redirect('/login')
    rents = db.query(History).order_by(History.isReturned.asc(), History.dateLoan.desc()).all()
    return render_template('rent-list.html', rents=rents, username=user.emailUser)

@app.route('/clear-cookie')
def clear_cookie():
    response = make_response(jsonify({"message": "Cookie cleared"}))
    response.set_cookie("email", '', expires=0)
    response.set_cookie("password", '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)