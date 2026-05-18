# 📰 News Project

## 📌 Project Overview

News Project is a full-stack Django web application that simulates a real-world digital publishing platform with role-based access control, editorial workflows, subscription systems, and REST API integration.

The system allows users to create, manage, review, approve, publish, and consume news content based on their assigned role while maintaining structured publishing processes and data integrity.

This project was designed to replicate professional newsroom workflows commonly used in modern publishing platforms.

---

# ✨ Core Features

## 👤 Reader
- Register and log in
- View published articles only
- Subscribe and unsubscribe to journalists
- Subscribe and unsubscribe to editorials
- Subscribe and unsubscribe to newsletters
- Access personalized content through the API

---

## ✍️ Journalist
- Create articles
- Edit and delete authored articles
- Create newsletters
- Join editorials
- Manage personal content

---

## 🛠️ Editor
- Review submitted articles
- Approve and publish articles
- Create and manage editorials
- Organize publishing workflows
- Publish content immediately

---

# 👥 User Roles

The application is built around three main user roles:

| Role | Responsibilities |
|------|------------------|
| Reader | Consumes and subscribes to content |
| Journalist | Creates and manages content |
| Editor | Reviews, approves, and organizes content |

Each role enforces strict permissions to simulate a real editorial publishing environment.

---

# 📰 Editorial Workflow

The application implements a structured article approval system:

1. A journalist creates an article
2. The article is saved as unpublished
3. An editor reviews the article
4. The editor approves and publishes it
5. Readers gain access to the published content

✔ This workflow replicates a real-world newsroom approval pipeline.

---

# 🗞️ Editorial System

Editorials act as publishing organizations that structure users and content.

### Features
- Journalists and editors can join editorials
- Articles are associated with editorials
- Readers can subscribe to editorials
- Editorials organize content distribution

✔ This feature improves content structure and system integrity.

---

# 🔔 Subscription System

Readers can dynamically interact with content through the frontend interface.

### Supported Subscriptions
- Journalists
- Editorials
- Newsletters

### Features
- Subscribe / unsubscribe directly from the UI
- Dynamic buttons update automatically
- Personalized subscription experience

✔ All subscription functionality is available through the frontend and backend.

---

# 📨 Newsletters

Newsletters provide curated collections of articles.

### Features
- Created by journalists
- Can include multiple articles
- Readers can subscribe
- Supports organized content distribution

---

# 🔌 REST API (Django REST Framework)

The project includes a fully functional REST API built with Django REST Framework.

---

## 🔐 Authentication Methods

- SessionAuthentication
- BasicAuthentication
- TokenAuthentication

---

## 🔑 Generate Authentication Token

```bash
python manage.py drf_create_token <username>
```

or:

```http
POST /api/token/
```

---

## 📡 Example API Endpoints

| Method | Endpoint | Description |
|------|--------|-------------|
| GET | /api/articles/ | List published articles |
| POST | /api/articles/ | Create article (journalist only) |
| GET | /api/articles/subscribed/ | View subscribed content |
| POST | /api/articles/<id>/approve/ | Approve article (editor only) |

---

# 🔒 Permissions Logic

The application enforces strict role-based permissions.

### Rules
- Only journalists can create articles
- Only editors can approve articles
- Readers can only view published content
- Journalists can only modify their own content
- Readers cannot modify platform content

✔ This ensures proper separation of responsibilities.

---

# ⚙️ Installation and Setup

## 1. Clone the repository

```bash
git clone <your-repository-url>
```

```bash
cd news_project
```

---

## 2. Create a virtual environment

```bash
python3 -m venv venv
```

---

## 3. Activate the virtual environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure environment variables

Create a `.env` file in the root directory and include:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=news_project_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

✔ These variables are required for Django and Docker configuration.

---

## 6. Run migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

## 7. Start the development server

```bash
python manage.py runserver
```

---

## 8. Open the application

```text
http://127.0.0.1:8000/
```

---

# 🐳 Running the Project with Docker

## Build and start containers

```bash
docker compose up --build
```

---

## Run migrations inside Docker

```bash
docker compose exec web python manage.py migrate
```

---

## Access the application

```text
http://localhost:8000/
```

---

# 🧪 Testing

Run automated tests with:

```bash
python manage.py test
```

---

## Manual Testing Included

- Role-based permissions
- REST API functionality
- Editorial workflows
- Subscription system
- Frontend interactions
- Authentication system

---

# 🧠 Code Quality

This project follows professional software development practices.

### Standards Used
- Black → code formatting
- Flake8 → PEP8 validation
- Modular Django architecture
- Separation of concerns
- Reusable application structure

---

# 🛠️ Technologies Used

- Python
- Django
- Django REST Framework
- MariaDB / MySQL
- HTML
- Django Templates
- Docker

---

# 📊 Project Planning

The project includes a dedicated Planning folder containing:

- Use Case Diagram
- API Sequence Diagram
- System Design Notes

---

# 🎯 Key Achievements

✔ Full role-based authentication system

✔ Editorial approval workflow

✔ Dynamic subscription system

✔ REST API with authentication

✔ Frontend and backend integration

✔ Clean and scalable architecture

✔ Docker containerization support

---

# 📌 Final Notes

This project demonstrates the development of a complete digital publishing platform that combines backend engineering, API development, role-based security, and interactive frontend behavior.

The application was designed to simulate real-world publishing systems while following professional software development standards.

---

# 👩‍💻 Author

Dania Onyebuagu