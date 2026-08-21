# Thefacebook - Django Social Network

A simplified recreation of the first 2004 Thefacebook experience built with Django. The app focuses on the original college-directory style: Harvard profiles, directory search, friends, pokes, classmates, and simple social-network stats.

## Features

- **User Authentication**: Register, login, logout
- **Harvard Profiles**: Profile picture, concentration, house, class year, courses, relationship status, interests, and about me
- **Directory Search**: Find classmates by name, concentration, house, or courses
- **Friends System**: Send, accept, reject, and remove friend requests
- **Pokes**: Send and clear pokes
- **Classmates**: Discover people taking the same course
- **Network Stats**: Show friends and friends-of-friends counts

## Setup

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```
   python manage.py migrate
   ```

3. **Create a superuser:**
   ```
   python manage.py createsuperuser
   ```

4. **Run the development server:**
   ```
   python manage.py runserver
   ```

5. **Open your browser:**
   Navigate to http://127.0.0.1:8000

## Project Structure

```
facebook/
├── accounts/         # User authentication, profiles, directory, classmates, pokes
├── friends/          # Friend requests and relationships
├── facebook_project/ # Django project settings
├── static/           # CSS and static files
├── templates/        # HTML templates
├── manage.py
└── requirements.txt
```

## Tech Stack

- Django 4.2+
- SQLite for local development
- HTML/CSS inspired by Thefacebook's 2004 interface
- Pillow for profile image handling
