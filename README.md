# News Project

## Project Description

News Project is a Django web application that allows users to interact with news articles and newsletters based on their assigned role.

The system includes three main user roles:

- Reader  
- Journalist  
- Editor  

Each role has different permissions and responsibilities within the application.

---

## Features

### Reader

Readers can:

- Register and log in  
- View published articles  
- Subscribe to journalists  
- Receive notifications when subscribed journalists publish new articles  

---

### Journalist

Journalists can:

- Register and log in  
- Create articles  
- Edit their own articles  
- Delete their own articles  
- Create newsletters  

Articles created by journalists are not published immediately. They must be approved by an editor first.

---

### Editor

Editors can:

- Review articles  
- Approve articles  
- Publish approved articles  
- Create editorials  

---

## Editorials

The application includes an Editorial model, which represents a publication (publisher).

Editorials allow journalists and editors to be grouped under a single publication. Articles are connected to an editorial, helping organize content and meeting the project requirements.

---

## API

The project includes API endpoints built with Django REST Framework.

Authentication is configured using:

- SessionAuthentication  
- BasicAuthentication  
- TokenAuthentication  

To generate a token, use:

bash python manage.py drf_create_token <username> 

Example endpoint:

POST /api/token/

---

## Code Style

This project includes code style tools to maintain clean and professional code.

Included in requirements.txt:

- Black  
- Flake8  

Black formats the code automatically, while Flake8 checks for PEP8 compliance.

---

## Technologies Used

- Python  
- Django  
- Django REST Framework  
- MariaDB / MySQL  
- HTML  
- Black  
- Flake8  

---

## Installation

1. Clone the repository:

bash git clone <your-repository-url> cd news_project 

2. Create and activate a virtual environment:

bash python3 -m venv venv source venv/bin/activate 

3. Install dependencies:

bash pip3 install -r requirements.txt 

4. Apply migrations:

bash python3 manage.py makemigrations python3 manage.py migrate 

5. Run the development server:

bash python3 manage.py runserver 

6. Open your browser and go to:

http://127.0.0.1:8000/

---

## Running Tests

To run automated tests:

bash python3 manage.py test 

---

## Planning

The project includes a Planning folder with:

- Use case diagram  
- API sequence diagram  
- Design notes  

These diagrams describe system behavior and API interactions.

---

## Notes

- Only journalists can create articles  
- Only editors can approve articles  
- Readers can only view published content  
- Articles are linked to editorials (publishers)  
- Newsletters can include multiple articles  

---