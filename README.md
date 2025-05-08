### 📖 **Library Management System**  
A FastAPI-based web application that allows users to manage books, rent them, and perform CRUD operations. Supports **user authentication**, **admin privileges**, and **database integration with SQLite and Flask**.

---

## ⚙️ **Installation & Setup**

### **1. Clone the Repository**
```bash
git clone https://github.com/lorenzober/Python-WEB-6-lab/LibraryProject.git
cd LibraryProject
```

### **2. Create a Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# On Windows: .venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install fastapi uvicorn sqlalchemy jinja2
```

### **4. Initialize the Database**
```bash
python -c 'from models import Base, engine; Base.metadata.create_all(bind=engine)'
```

### **5. Run the FastAPI Server**
```bash
uvicorn main:app --reload
```

FastAPI will now be running at:  
- **Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **Login Page:** [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)  
- **Books List:** [http://127.0.0.1:8000/book-list](http://127.0.0.1:8000/book-list)  

---

## 🔑 **User Authentication**
Users can **register** and **log in** using email and password. Authentication is handled using **cookies**.

### **Register a New User**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/registration' \
     -H 'Content-Type: application/json' \
     -d '{"nameUser": "John", "surnameUser": "Doe", "emailUser": "john@example.com", "passwordUser": "1234", "numberUser": "1234567890"}'
```

### **Login User**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/login' \
     -H 'Content-Type: application/json' \
     -d '{"emailUser": "john@example.com", "passwordUser": "1234"}'
```

### **Promote User to Admin**
Run the following script and enter the email of the user:
```bash
python permission.py
```

---

## 📚 **Book Management**
Admins can **add, update, and delete books**, while users can **view and rent books**.

### **Get All Books**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/book-list'
```

### **Add a New Book (Admin Only)**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/book' \
     -H 'Content-Type: application/json' \
     -d '{"nameBook": "Python Basics", "yearBook": 2023, "availableBook": 5, "category_id": 1, "author_id": 1}'
```

### **Edit a Book (Admin Only)**
```bash
curl -X 'PUT' 'http://127.0.0.1:8000/book' \
     -H 'Content-Type: application/json' \
     -d '{"id": 1, "nameBook": "Python Advanced", "yearBook": 2024, "availableBook": 10, "category_id": 1, "author_id": 1}'
```

### **Delete a Book (Admin Only)**
```bash
curl -X 'DELETE' 'http://127.0.0.1:8000/book/1'
```

---

## 📖 **Renting Books**
Users can **rent** and **return books**.

### **Rent a Book**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/book/1/rent'
```

---

## 🎨 **Frontend Integration**
- Uses **Jinja2 templates** for **server-side rendering**.
- **Bootstrap 5** for styling.

---

## 🔥 **Technologies Used**
- **FastAPI** - Web framework
- **SQLite & SQLAlchemy** - Database & ORM
- **Jinja2** - Template rendering
- **Bootstrap 5** - Frontend styling
- **Uvicorn** - ASGI server

---

## 📝 **To-Do / Future Improvements**
- ✅ User authentication with hashed passwords  
- ✅ Admin panel for managing books  
- ⏳ Implement JWT authentication  
- ⏳ Add user profiles  
- ⏳ Deploy to **Heroku/Vercel**  

---

### 💡 **Contributions**
Feel free to fork this repository and submit a **Pull Request**! 😊

---
🚀 **Enjoy your Library Management System!**  
Let me know if you need any modifications! 🚀# Python-WEB-3-lab
# Python-WEB-6-lab
