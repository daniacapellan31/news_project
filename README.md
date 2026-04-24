# News Project

## Project Description

News Project is a Django web application that allows users to interact with news articles and newsletters based on their assigned role.

The system includes three main user roles:

- Reader
- Journalist
- Editor

Each role has different permissions and responsibilities within the application.

## Features

### Reader

Readers can:

- Register and log in
- View published articles
- Subscribe to journalists
- Receive notifications when subscribed journalists publish new articles

### Journalist

Journalists can:

- Register and log in
- Create articles
- Edit their own articles
- Delete their own articles
- Create newsletters

Articles created by journalists are not published immediately. They must be approved by an editor first.

### Editor

Editors can:

- Review articles
- Approve articles
- Publish approved articles
- Create editorials

## Editorials

The application includes an Editorial model. Editorials allow journalists and editors to be grouped under a publication.

Articles are connected to an editorial, which helps organize the content and reflects the structure required by the project.

## API

The project includes API endpoints built with Django REST Framework.

Authentication is configured using:

- SessionAuthentication
- BasicAuthentication
- TokenAuthentication

The API requires authenticated users.

## Code Style

This project includes code style tools to help maintain clean and professional code.

The following tools are included in `requirements.txt`:

- Black
- Flake8

Black is used to format the code automatically, and Flake8 is used to check for PEP8 style issues.

## Technologies Used

- Python
- Django
- Django REST Framework
- MariaDB / MySQL
- HTML
- Black
- Flake8

## Installation

1. Clone the repository or download the project files.

2. Create and activate a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate