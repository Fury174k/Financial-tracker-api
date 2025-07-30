# Finance API

A Django RESTful API for managing personal finances, including user authentication (standard and Google OAuth), expense tracking, and account management. This project is designed to serve as the backend for a financial tracking web application.

---

## Features

- **User Registration & Authentication**
  - Register with username, email, password, and optional profile picture
  - Login with username/email and password
  - Google OAuth login support
- **Expense Management**
  - Create, read, update, and delete expenses
  - Categorize expenses and associate with accounts
- **Account Management**
  - Manage multiple financial accounts per user
- **Profile Picture Support**
  - Upload and retrieve user profile pictures
- **CORS Support**
  - Configured for frontend integration (e.g., React on Vercel)
- **Token Authentication**
  - Uses DRF token authentication for secure API access

---

## Tech Stack

- **Backend:** Django 5.x, Django REST Framework
- **Database:** SQLite (development), supports PostgreSQL for production
- **Authentication:** Django Auth, DRF Token Auth, Google OAuth
- **Media:** Handles user-uploaded profile pictures

---

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Finance_Api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **(Optional) Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

---

## Environment Variables

- `SECRET_KEY`: Django secret key (keep this secret in production)
- `DATABASE_URL`: (Optional) Set for production database (e.g., PostgreSQL)
- Google OAuth credentials as required

---

## API Endpoints

- `/api/register/` — Register a new user
- `/api/login/` — Login with username/email and password
- `/api/auth/google/` — Google OAuth login
- `/api/expenses/` — CRUD for expenses (authenticated)
- `/api/accounts/` — CRUD for accounts (authenticated)
- `/api/profile/` — Get or update user profile

---

## Media & Static Files

- User profile pictures are stored in `/media/profile_pics/`
- In development, media files are served automatically
- In production, configure your web server to serve media files

---

## CORS

- Allowed origins include your deployed frontend and local development (`localhost:3000`, Vercel domains, etc.)

---

## Deployment

- Ready for deployment on platforms like Render, Heroku, etc.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` and `DATABASE_URL` for production

---

## License

MIT License

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Contact

For questions or support, please contact the project maintainer.
