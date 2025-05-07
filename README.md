# CharitySpark

CharitySpark is a modern crowdfunding platform built with Django and Django REST Framework. It connects donors with impactful campaigns, allowing users to create, manage, and support charitable initiatives.

## Features
- User registration, login, and profile management
- Campaign creation, editing, and listing
- Category-based campaign filtering
- Donation system with simulated payment (demo only)
- RESTful API for all major resources (users, campaigns, donations, categories)
- Responsive Bootstrap 5 UI with custom theming
- Admin panel for managing users, campaigns, and donations
- Sample data and images for demo purposes

## How I Made This App
1. **Project Setup**
   - Created a new Django project and apps: `accounts`, `campaigns`, `donations`, and `api`.
   - Installed dependencies: Django, djangorestframework, Pillow, crispy-forms, crispy-bootstrap4, requests, python-dotenv.
   - Configured settings for static/media files, authentication, and REST framework.

2. **Models & Database**
   - Defined models for UserProfile, Category, Campaign, and Donation.
   - Used Django signals to auto-create user profiles.
   - Added properties to Campaign for progress, completion, and days remaining.
   - Created migrations and migrated the database.

3. **API Development**
   - Built REST API endpoints using Django REST Framework (DRF) viewsets and serializers.
   - Implemented custom permissions for campaign ownership.
   - Added endpoints for registration, login, and user profile.

4. **Frontend & Templates**
   - Designed responsive templates using Bootstrap 5 and Font Awesome.
   - Used crispy-forms for form rendering.
   - Implemented JavaScript for AJAX form submissions and dynamic UI updates.
   - Created pages for campaign browsing, donation, user dashboard, and static info (About, Impact).

5. **Authentication**
   - Used DRF token authentication for API endpoints.
   - Managed tokens and user info in localStorage for seamless SPA-like experience.
   - Provided login, registration, and logout flows with client-side and server-side support.

6. **Sample Data & Images**
   - Added management commands to generate sample users, campaigns, donations, and images for demo/testing.

7. **Admin Panel**
   - Customized Django admin for easy management of users, campaigns, and donations.

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
5. **(Optional) Load sample data:**
   ```bash
   python manage.py create_sample_data
   python manage.py add_sample_images
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   - Open [http://localhost:8000/](http://localhost:8000/) in your browser.

## Development Notes
- All API endpoints are under `/api/`.
- Static and media files are served in development mode.
- Demo payment: No real transactions are processed.
- For production, set `DEBUG = False` and configure allowed hosts, static/media storage, and secret keys.

## Credits
- Built with Django, DRF, Bootstrap, and Font Awesome.
- Demo images from [Pexels](https://pexels.com) and [Picsum](https://picsum.photos).

---
Feel free to fork, modify, and use this project for your own charity or crowdfunding ideas!
