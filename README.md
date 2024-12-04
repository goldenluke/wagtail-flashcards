# MemorAI: Flashcards Application

A dynamic flashcard application built with Django and Wagtail for effective learning and memorization.

## 📖 Overview
**MemorAI** is an interactive platform for creating, managing, and reviewing flashcards. Designed with Wagtail CMS and Django, it supports personalized learning with features like media attachments, difficulty categorization, and user-specific dashboards.

## 🎯 Features
- **Flashcard Creation**: Create flashcards with media (images, videos, etc.).
- **User Dashboard**: Personalized dashboard with categories and folders.
- **Difficulty Tracking**: Mark flashcards as easy, medium, or hard.
- **Responsive UI**: Designed for desktop and mobile use.
- **Wagtail Integration**: Leverages Wagtail CMS for content management.
- **Google Authentication**: Easily log in with Google using Allauth.

## 🛠️ Tech Stack
- **Backend**: Django 5.1, Wagtail 6.3
- **Frontend**: HTML, CSS (with Google Fonts Icons), JavaScript
- **Database**: SQLite (default, configurable)
- **Authentication**: Allauth for user management

## 🚀 Installation and Setup

### Prerequisites
- Python 3.10+
- Pipenv or virtualenv for dependency management

### Step 1: Clone the Repository
```bash
git clone https://github.com/goldenluke/wagtail-flashcards.git/
cd MemorAI
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Apply Migrations
```bash
python manage.py migrate
```

### Step 4: Run the Development Server
```bash
python manage.py runserver
```
Access the app at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 🧩 Project Structure
```plaintext
MemorAI/
├── flashcards/          # Core app for flashcard management
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── media/               # Uploaded media files
├── wagtail/             # Wagtail-specific integrations
├── manage.py            # Django management script
└── requirements.txt     # Project dependencies
```

## 📘 Usage

### Creating Flashcards
1. Log in to your account.
2. Navigate to the "Create Flashcard" page.
3. Fill in the question, answer, and attach media if required.

### Managing Flashcards
- **Mark Difficulty**: Use the interface to mark flashcards as "Easy," "Medium," or "Hard."
- **Flip and Navigate**: Flip flashcards to view answers and navigate through decks.

### Admin Features
- Wagtail admin panel for managing pages and flashcard categories.
- Assign permissions to user groups like "Player."

## 🛡️ Security
This project uses Django's built-in security features:
- CSRF protection
- Secure authentication with Allauth

## 👥 Contributing
We welcome contributions! Please:
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Feature description"`).
4. Push to your fork and open a Pull Request.

## 📄 License
This project is licensed under the MIT License.

## 💌 Acknowledgments
- Built using [Django](https://www.djangoproject.com/) and [Wagtail](https://wagtail.org/).
- Icons from [Google Fonts](https://fonts.google.com/icons).

---

Have any questions? Feel free to [open an issue](https://github.com/your-username/MemorAI/issues)!
