# Quick Start Guide - Tourism Bot Admin Panel

## 🚀 Getting Started in 3 Steps

### Step 1: Verify Setup
```bash
cd /Users/ibrohim/PycharmProjects/TourismBot
python check_setup.py
```

### Step 2: Start the Application
```bash
cd web
python run_admin.py
```

### Step 3: Access the Admin Panel
Open your browser and go to: **http://localhost:8000/admin**

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 📋 What's New & Improved

### ✨ Enhanced Admin Panel
1. **Better columns display** - Added relationship viewing
2. **Improved pagination** - 20 items per page
3. **Better labels** - Clear column headers
4. **Validation messages** - Helpful field descriptions
5. **Formatted display** - City names shown in uppercase

### 🔌 New REST API
Complete CRUD API at `/api`:
- Full CRUD operations for Cities, Excursions, and Points
- Input validation with Pydantic models
- Proper error handling
- Auto-generated docs at `/docs`

### 🔒 Enhanced Security
- Better authentication handling
- Session management
- Input sanitization
- Validation on all endpoints

### 📚 Documentation
- Full API documentation at `/api/docs`
- Quick start guide (this file)
- Comprehensive ADMIN_GUIDE.md with examples
- Setup validation script

---

## 🎯 Common Tasks

### Adding a New City
1. Go to Admin Panel → Cities
2. Click "Create+" button
3. Enter city name (e.g., "Paris")
4. Click Save

### Adding an Excursion to a City
1. Go to Admin Panel → Excursions
2. Click "Create+" button
3. Select city from dropdown
4. Enter title (e.g., "Eiffel Tower Tour")
5. Enter description (minimum 10 characters)
6. Click Save

### Adding a Point to an Excursion
1. Go to Admin Panel → Excursion Points
2. Click "Create+" button
3. Select excursion
4. Enter order number (1-100)
5. Enter title and description
6. Enter latitude and longitude
7. Optionally add image/audio paths
8. Click Save

---

## 🔌 Using the API

### Get All Cities
```bash
curl http://localhost:8000/api/cities
```

### Create a City (Python)
```python
import requests

response = requests.post(
    "http://localhost:8000/api/cities",
    json={"name": "Tokyo"}
)
print(response.json())
```

### Get Points for an Excursion
```bash
curl http://localhost:8000/api/points?excursion_id=1
```

---

## 📁 File Structure Overview

```
TourismBot/
├── web/
│   ├── admin.py          ✨ Enhanced admin configurations
│   ├── auth.py           🔒 Improved authentication
│   ├── main.py           🔌 FastAPI app with new API routes
│   ├── crud.py           🆕 Complete CRUD API endpoints
│   ├── run_admin.py      Launch script
│   ├── ADMIN_GUIDE.md    📚 Detailed documentation
│   └── README.md         Original readme
├── db/
│   ├── models.py         Data models
│   ├── base.py           SQLAlchemy base
│   └── session.py        ✨ Added get_async_session()
├── check_setup.py        🆕 Setup validation script
├── requirements.txt      Dependencies
└── db.sqlite3            Database (created on first run)
```

---

## ⚙️ Configuration

### Change Admin Credentials
Edit `.env` file:
```env
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
```

### Change Database
Update `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't connect to admin | Make sure app is running on http://localhost:8000 |
| Login fails | Check .env file for correct ADMIN_USERNAME and ADMIN_PASSWORD |
| API returns 404 | Make sure you're using correct endpoint URLs |
| Validation errors | Check field length requirements in error messages |
| Foreign key errors | Ensure referenced city/excursion exists |

---

## 📖 More Information

For detailed information, see:
- **[ADMIN_GUIDE.md](ADMIN_GUIDE.md)** - Complete feature documentation
- **http://localhost:8000/docs** - Interactive API documentation
- **http://localhost:8000/redoc** - API documentation (ReDoc)

---

## 🎓 Learning More

### Admin Panel Features
- Search by name/title
- Sort by any column
- Batch operations
- Relationship viewing
- Form validation with helpful hints

### API Features
- RESTful design
- Proper HTTP status codes
- Input validation
- Error messages
- OpenAPI documentation

### Database
- SQLAlchemy ORM
- Async operations
- Relationship management
- Foreign key constraints

---

## 💡 Pro Tips

1. **Use the Admin Panel** for quick edits and browsing
2. **Use the API** for integrations and automation
3. **Check /docs** for interactive API testing
4. **Filter by city/excursion** to reduce clutter
5. **Use proper coordinates** - Google Maps can help find them

---

**Need more help?** Check the detailed [ADMIN_GUIDE.md](ADMIN_GUIDE.md) file!
