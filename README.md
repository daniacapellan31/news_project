# 📰 News Project

## 📌 Project Overview

News Project is a full-stack Django web application that simulates a real-world news publishing platform with role-based access control and API integration.

Users can create, manage, approve, and consume news content depending on their assigned role.

---

## 👥 User Roles

The system is built around three core roles:

- Reader – consumes content  
- Journalist – creates content  
- Editor – reviews and approves content  

Each role has strictly controlled permissions to ensure proper workflow and data integrity.

---

## ✨ Core Features

### 👤 Reader
- Register and log in  
- View only published articles  
- Subscribe to journalists  
- View articles from subscribed journalists via API  

---

### ✍️ Journalist
- Create articles (initially unpublished)  
- Edit and delete their own articles  
- Create newsletters  
- Manage their own content  

---

### 🛠️ Editor
- Review submitted articles  
- Approve articles via API  
- Publish content to make it visible to readers  
- Manage editorials (publications)  

---

## 📰 Articles Workflow

1. Journalist creates an article  
2. Article is saved as Not Published  
3. Editor approves article via API  
4. Article becomes Published  
5. Readers can now view it  

✔ This workflow demonstrates real-world editorial approval systems.

---

## 🗞️ Editorials

Editorials act as publishers that group journalists and editors.

- Articles belong to an editorial  
- Editors manage approval within their editorial  
- Journalists publish under a structured organization  

---

## 📨 Newsletters

- Created by journalists  
- Can include multiple articles  
- Readers can subscribe to newsletters  
- Provides curated collections of content  

---

## 🔌 API (Django REST Framework)

The project includes a fully functional REST API.

### 🔐 Authentication Methods
- SessionAuthentication  
- BasicAuthentication  
- TokenAuthentication  

---

### 🔑 Generate Token

bash python manage.py drf_create_token <username> 

or:

bash POST /api/token/ 

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

---

## 🧪 Testing

Run tests with:

bash python3 manage.py test 

Manual testing was also performed to validate:
- Role permissions  
- API functionality  
- UI behavior  

---

## 🧠 Code Quality

This project follows professional coding standards:

- Black → automatic formatting  
- Flake8 → PEP8 validation  

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
bash git clone <your-repository-url> cd news_project 

### 2. Create virtual environment
bash python3 -m venv venv source venv/bin/activate 

### 3. Install dependencies
bash pip install -r requirements.txt 

### 4. Run migrations
bash python manage.py makemigrations python manage.py migrate 

### 5. Run server
bash python manage.py runserver 

### 6. Open browser
http://127.0.0.1:8000/

---

## 📊 Project Planning

The project includes a Planning folder with:

- Use Case Diagram  
- API Sequence Diagram  
- System Design Notes  

These documents describe system architecture and behavior.

---

## 🎯 Key Achievements

- Full role-based system  
- Secure API with token authentication  
- Editorial approval workflow  
- Integration between UI and API  
- Clean and maintainable code  

---

## 📌 Final Notes

This project demonstrates the implementation of a real-world publishing workflow, combining backend logic, API design, and frontend interaction in a structured and scalable way.

---

## 👩‍💻 Author

Dania Onyebuagu