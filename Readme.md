This is project for Sweet shop mangement.
The tech stack used here will be Python(Fast Api)+ Frontend(React) + MongoDB(ATLAS)

# 🍬 Sweet Shop Management System (TDD Kata)

## 📌 Project Overview
This project is a **Sweet Shop Management System** developed as part of a **Test-Driven Development (TDD) Kata**.  
It provides a secure and scalable backend API to manage sweets, inventory, and users with proper authentication and role-based authorization.

The backend is built using **FastAPI** and **MongoDB**, following clean architecture principles and fully tested using **pytest**.

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI  
- **Database:** MongoDB (Atlas)  
- **Authentication:** JWT (Token-based)  
- **Testing:** Pytest (TDD)  
- **API Style:** RESTful  
- **Frontend:** React (separate / planned)

---

## 🔐 Features

### Authentication & Authorization
- User registration and login
- JWT-based authentication
- Role-based access control (User / Admin)

### Sweets Management
- Add new sweets
- View all sweets
- Update sweet details
- Delete sweets (Admin only)

### Inventory Management
- Purchase sweets (reduces quantity)
- Restock sweets (Admin only)

### System
- Health check endpoint
- MongoDB indexes initialized on application startup

---

## 🌐 API Endpoints

### Auth
- `POST /register` – Register a new user  
- `POST /login` – Login and receive JWT token  

### Sweets (Protected)
- `POST /sweets` – Add a sweet  
- `GET /sweets` – Get all sweets  
- `PUT /sweets/{id}` – Update sweet  
- `DELETE /sweets/{id}` – Delete sweet (Admin only)

### Inventory
- `POST /sweets/{id}/purchase` – Purchase sweet  
- `POST /sweets/{id}/restock` – Restock sweet (Admin only)

### Health
- `GET /health` – Application health check  

---

## 🚀 How to Run the Backend

### 1️⃣ Create Virtual Environment
```md
python -m venv venv
```
- `source venv/bin/activate   # Linux / Mac`
- `venv\Scripts\activate      # Windows`

### 2️⃣ Install Dependencies
pip install fastapi uvicorn pymongo python-jose passlib pytest


### 3️⃣ Configure Environment Variables
Create a .env file or set variables:

MONGODB_URL=<your_mongodb_atlas_url>
JWT_SECRET_KEY=<your_secret_key>

### 4️⃣ Run the Server
uvicorn app.main:app --reload

## Running Tests (TDD)
All features were implemented using Test-Driven Development.
Run all tests: 
pytest

