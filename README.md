# 📰 News Project

## 📌 Project Overview

News Project is a full-stack Django web application that simulates a real-world news publishing platform with role-based access control, editorial workflows, and API integration.

The system allows users to create, manage, approve, and consume news content based on their assigned role while maintaining data integrity and structured publishing processes.

---

## 👥 User Roles

The application is built around three core roles:

- Reader – consumes and subscribes to content  
- Journalist – creates and manages content  
- Editor – reviews, approves, and organizes content  

Each role enforces strict permission rules to replicate a real editorial system.

---

## ✨ Core Features

### 👤 Reader
- Register and log in  
- View only published articles  
- Subscribe to journalists  
- Subscribe to editorials (publishers)  
- Subscribe to newsletters  
- View personalized content via API  

---

### ✍️ Journalist
- Create articles (initially unpublished)  
- Edit and delete their own articles  
- Create newsletters  
- Join editorials (publishers)  
- Manage authored content  

---

### 🛠️ Editor
- Review submitted articles  
- Approve and publish articles  
- Create and manage editorials  
- Join editorials  
- Publish content immediately  

---

## 📰 Articles Workflow

1. Journalist creates an article  
2. Article is saved as Not Published  
3. Editor reviews and approves the article  
4. Article becomes Published  
5. Readers can access the content  

✔ This replicates a real editorial approval pipeline.

---

## 🗞️ Editorial System (Key Improvement)

Editorials act as publishers that organize content and users.

- Journalists and editors can join editorials
- Articles are linked to an editorial
- Readers can subscribe to editorials
- Editorials provide structured content grouping

✔ This feature was implemented to meet project requirements and improve system integrity.

---

## 🔔 Subscription System (Key Improvement)

Readers can now interact dynamically through the UI:

- Subscribe / Unsubscribe to journalists  
- Subscribe / Unsubscribe to editorials  
- Subscribe / Unsubscribe to newsletters  

✔ All interactions are available through the frontend (not only admin)

✔ UI buttons dynamically update based on subscription state

---

## 📨 Newsletters

- Created by journalists  
- Can include multiple articles  
- Readers can subscribe  
- Provides curated content collections  

---

## 🔌 API (Django REST Framework)

The project includes a fully functional REST API.

### 🔐 Authentication Methods
- SessionAuthentication  
- BasicAuthentication  
- TokenAuthentication  

---

### 🔑 Generate Token

    python manage.py drf_create_token <username>

or:

    POST /api/token/

---

### 📡 Example Endpoints

| Method | Endpoint | Description |
|------|--------|-------------|
| GET | /api/articles/ | List published articles |
| POST | /api/articles/ | Create article (journalist only) |
| GET | /api/articles/subscribed/ | Articles from subscriptions |
| POST | /api/articles/<id>/approve/ | Approve article (editor only) |

---

## 🔒 Permissions Logic

- Only journalists can create articles  
- Only editors can approve articles  
- Only published articles are visible to readers  
- Journalists can only edit their own content  
- Readers can only subscribe (not modify content)  

---

## 🧪 Testing

Run tests with:

    python manage.py test

Manual testing was performed to validate:

- Role-based permissions  
- API functionality  
- Subscription system  
- UI interaction (buttons and feedback messages)  

---

## 🧠 Code Quality

This project follows professional development standards:

- Black → code formatting  
- Flake8 → PEP8 validation  
- Modular Django structure  
- Clear separation of concerns  

---

## 🛠️ Technologies Used

- Python  
- Django  
- Django REST Framework  
- MariaDB / MySQL  
- HTML (Django Templates)  

---

## ⚙️ Installation Guide

### 1. Clone repository

    git clone <your-repository-url>
    cd news_project

### 2. Create virtual environment

    python3 -m venv venv
    source venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Run migrations

    python manage.py makemigrations
    python manage.py migrate

### 5. Run server

    python manage.py runserver

### 6. Open in browser

    http://127.0.0.1:8000/

---

## 📊 Project Planning

The project includes a Planning folder with:

- Use Case Diagram  
- API Sequence Diagram  
- System Design Notes  

---

## 🎯 Key Achievements

- Full role-based system  
- Editorial workflow implementation  
- Dynamic subscription system (UI + backend)  
- REST API with authentication  
- Clean and scalable architecture  

---

## 📌 Final Notes

This project demonstrates a complete real-world publishing system, combining backend logic, API design, and interactive frontend behavior.

---

## Local Setup (venv)

### 1. Create virtual environment
python3 -m venv venv

### 2. Activate it
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run migrations
python manage.py migrate

### 5. Run server
python manage.py runserver

---

## Running the project with Docker

### 1. Build and start containers
docker compose up --build

### 2. Run migrations (first time only)
docker compose exec web python manage.py migrate

### Access the application
http://localhost:8000/

---

## Notes

- Do not include sensitive information such as passwords or API keys.

## 👩‍💻 Author

Dania Ony