# Facebook Clone - Django Social Network

A simplified Facebook clone built with Django featuring user profiles, friends system, news feed, posts, comments, and likes.

## Features

- **User Authentication**: Register, login, logout
- **User Profiles**: Profile pictures, cover photos, bio, location, and more
- **Friends System**: Send, accept, reject friend requests
- **News Feed**: See posts from friends
- **Posts**: Create posts with text and images
- **Comments**: Comment on posts
- **Likes**: Like/unlike posts

## Setup

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```
   python manage.py makemigrations
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
├── accounts/         # User authentication and profiles
├── posts/            # Posts, comments, and likes
├── friends/          # Friend requests and relationships
├── facebook_project/ # Django project settings
├── static/           # CSS and static files
├── templates/        # HTML templates
├── manage.py
└── requirements.txt
```

## Tech Stack

- Django 4.2+
- SQLite (default database)
- HTML/CSS (no JavaScript framework)
- Pillow (image handling)
