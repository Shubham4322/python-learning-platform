# Python Learning Platform

A web-based platform for learning Python programming with interactive theory and practice questions.

## Features

- 📚 **Theory-based Learning**: Read concepts before practicing
- 💻 **Code Editor**: Write and run Python code in browser
- ✅ **Auto-checking**: Instant feedback on code submissions
- 🔓 **Progressive Unlocking**: Complete topics to unlock new ones
- 📊 **Progress Tracking**: Track your learning journey

## Tech Stack

### Backend
- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite Database
- JWT Authentication

### Frontend
- React 18
- Vite
- React Router
- Axios

## Setup Instructions

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver