# 📚 Notes & PYQ Sharing Platform

A full-stack web platform where college students can upload, browse, and download academic notes and previous year question papers (PYQs), organized by subject and semester.

🔗 **Live Demo:** [https://notes-platform-1.onrender.com](https://notes-platform-1.onrender.com)

---

## ✨ Features

- **User Authentication** — Secure signup/login system using JWT (JSON Web Tokens) and bcrypt password hashing
- **Upload Resources** — Authenticated users can upload notes and PYQs with metadata (subject, semester, type, year)
- **Browse & Filter** — Browse all resources with filters for semester, subject, and resource type (case-insensitive search)
- **Download** — One-click download of any resource, served via Cloudinary CDN
- **Cloud Storage** — Files are stored on Cloudinary (not the server), ensuring persistence across deployments
- **Persistent Database** — PostgreSQL database hosted on Render for reliable, permanent data storage

---

## 🛠️ Tech Stack

**Backend:**
- Python, FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (database)
- JWT (python-jose) for authentication
- Passlib (bcrypt) for password hashing
- Cloudinary for file storage

**Frontend:**
- HTML, CSS, JavaScript (vanilla)
- Fetch API for backend communication

**Deployment:**
- Backend & Frontend hosted on Render
- Database hosted on Render PostgreSQL
- File storage on Cloudinary

---

## 📂 Project Structure

```
notes-platform/
├── main.py                 # FastAPI app & routes
├── models.py                # SQLAlchemy database models
├── schemas.py                # Pydantic request/response schemas
├── database.py               # Database connection setup
├── auth.py                   # Password hashing & JWT logic
├── dependencies.py           # Auth dependency (get_current_user)
├── cloudinary_config.py      # Cloudinary configuration
├── requirements.txt          # Python dependencies
└── frontend/
    ├── index.html             # Login/Signup page
    ├── resources.html         # Browse & filter resources
    └── upload.html            # Upload new resources
```

---

## 🔑 Key Concepts Implemented

- RESTful API design with FastAPI
- JWT-based stateless authentication
- Password security with bcrypt hashing
- File upload handling with cloud storage integration
- Environment variable management for secrets (`.env`)
- CORS configuration for frontend-backend communication
- Database ORM with SQLAlchemy

---

## 🚀 Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/Bhumikapapnai/notes-platform.git
   cd notes-platform
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   SECRET_KEY=your_jwt_secret_key
   DATABASE_URL=your_postgresql_connection_string
   CLOUD_NAME=your_cloudinary_cloud_name
   CLOUDINARY_API_KEY=your_cloudinary_api_key
   CLOUDINARY_API_SECRET=your_cloudinary_api_secret
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

5. Open `frontend/index.html` in your browser (update `API_URL` to `http://127.0.0.1:8000` for local testing).

---

## 📌 Future Improvements

- Search by title
- Delete/edit own uploaded resources
- Upvote/rating system for resources
- Admin dashboard for moderation

---

## 👤 Author

Bhumika Papnai