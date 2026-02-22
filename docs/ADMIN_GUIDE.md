# Tourism Bot Admin & CRUD System

## Overview

This is a comprehensive admin panel and RESTful API for managing tourism data including cities, excursions, and points of interest.

## Features

### Admin Panel (SQLAdmin)
- **Visual admin interface** accessible at `/admin`
- **Full CRUD operations** for Cities, Excursions, and Points
- **Search & filtering** capabilities
- **Form validation** with helpful descriptions
- **Secure authentication** with session-based login

### RESTful API
- Complete CRUD API endpoints for all resources
- Input validation with Pydantic models
- Proper HTTP status codes and error handling
- OpenAPI documentation at `/docs`

## Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### Running the Application
```bash
cd web
python run_admin.py
```

The admin panel will be available at: `http://localhost:8000/admin`

## Admin Panel Usage

### Logging In
1. Navigate to `http://localhost:8000/admin`
2. Enter username and password (default: `admin` / `admin123`)
3. Click "Login"

### Managing Cities
1. Click on "Cities" in the left sidebar
2. **View all cities**: See the list with search and sort options
3. **Create a city**: Click "Create+" button and fill in the city name
4. **Edit a city**: Click on the city name to open the edit form
5. **Delete a city**: Click the trash icon next to the city

### Managing Excursions
1. Click on "Excursions" in the left sidebar
2. **View all excursions**: Filter by city using search
3. **Create an excursion**:
   - Click "Create+" button
   - Select a city from the dropdown
   - Enter title (5-200 characters)
   - Enter detailed description (10-2000 characters)
   - Click "Save"
4. **Edit an excursion**: Click on the excursion title
5. **Delete an excursion**: Click the trash icon

### Managing Excursion Points
1. Click on "Excursion Points" in the left sidebar
2. Points are automatically sorted by excursion and order
3. **Create a point**:
   - Click "Create+" button
   - Select an excursion
   - Enter order number (1-100)
   - Enter title (3-200 characters)
   - Enter text/description (10-2000 characters)
   - Enter latitude (-90 to 90)
   - Enter longitude (-180 to 180)
   - Optionally add audio and image paths
   - Click "Save"
4. **Edit a point**: Click on the point title
5. **Delete a point**: Click the trash icon

## API Endpoints

### Cities
- `GET /api/cities` - Get all cities
- `POST /api/cities` - Create a new city
- `GET /api/cities/{city_id}` - Get a specific city
- `PUT /api/cities/{city_id}` - Update a city
- `DELETE /api/cities/{city_id}` - Delete a city

### Excursions
- `GET /api/excursions` - Get all excursions (with optional `city_id` filter)
- `POST /api/excursions` - Create a new excursion
- `GET /api/excursions/{excursion_id}` - Get a specific excursion
- `PUT /api/excursions/{excursion_id}` - Update an excursion
- `DELETE /api/excursions/{excursion_id}` - Delete an excursion

### Points
- `GET /api/points` - Get all points (with optional `excursion_id` filter)
- `POST /api/points` - Create a new point
- `GET /api/points/{point_id}` - Get a specific point
- `PUT /api/points/{point_id}` - Update a point
- `DELETE /api/points/{point_id}` - Delete a point

## API Usage Examples

### Using cURL

#### Get all cities
```bash
curl http://localhost:8000/api/cities
```

#### Create a city
```bash
curl -X POST http://localhost:8000/api/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "Paris"}'
```

#### Get excursions for a city
```bash
curl http://localhost:8000/api/excursions?city_id=1
```

#### Create an excursion
```bash
curl -X POST http://localhost:8000/api/excursions \
  -H "Content-Type: application/json" \
  -d '{
    "city_id": 1,
    "title": "Eiffel Tower Tour",
    "description": "A guided tour of the iconic Eiffel Tower with historical details"
  }'
```

#### Create a point
```bash
curl -X POST http://localhost:8000/api/points \
  -H "Content-Type: application/json" \
  -d '{
    "excursion_id": 1,
    "order": 1,
    "title": "Tower Base",
    "text": "Starting at the base of the Eiffel Tower",
    "lat": 48.858370,
    "lng": 2.294481,
    "image": "media/images/tower_base.jpg",
    "audio": "media/audio/tower_intro.mp3"
  }'
```

### Using Python Requests
```python
import requests

# Get all cities
response = requests.get("http://localhost:8000/api/cities")
cities = response.json()

# Create a new city
new_city = requests.post(
    "http://localhost:8000/api/cities",
    json={"name": "Tokyo"}
)
city_id = new_city.json()["id"]

# Create an excursion
new_excursion = requests.post(
    "http://localhost:8000/api/excursions",
    json={
        "city_id": city_id,
        "title": "Traditional Temple Tour",
        "description": "Visit the most famous temples in Tokyo"
    }
)
```

## Validation Rules

### City
- **name**: Required, 2-100 characters

### Excursion
- **city_id**: Required (must exist)
- **title**: Required, 5-200 characters
- **description**: Required, 10-2000 characters

### Point
- **excursion_id**: Required (must exist)
- **order**: Required, 1-100
- **title**: Required, 3-200 characters
- **text**: Required, 10-2000 characters
- **lat**: Required, -90 to 90
- **lng**: Required, -180 to 180
- **audio**: Optional, max 255 characters
- **image**: Optional, max 255 characters

## File Structure

```
web/
├── admin.py          # Admin panel configuration
├── auth.py           # Authentication backend
├── main.py           # FastAPI application setup
├── crud.py           # CRUD API routes (new)
└── run_admin.py      # Application launcher
```

## Features in Detail

### Form Validation
All forms include:
- Required field validation
- Length constraints
- Type validation
- Helpful error messages
- Descriptive field hints

### Search & Filtering
- **Cities**: Search by name
- **Excursions**: Search by title or description, filter by city
- **Points**: Search by title or text, filter by excursion

### Sorting
- Cities: By ID or name
- Excursions: By ID, title, or city
- Points: Default sorted by excursion and order

### Security
- Session-based authentication
- Secure logout
- Protected admin routes
- CSRF protection via SessionMiddleware

## Troubleshooting

### Can't login to admin panel
- Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`
- Default credentials are `admin` / `admin123`
- Clear browser cookies and try again

### Foreign key errors when creating records
- Ensure the referenced city/excursion exists
- Check the ID in the dropdown/form
- Use the API docs to verify available resources

### Validation errors
- Check the error message for specific requirements
- Ensure all required fields are filled
- Verify character length constraints are met

## Next Steps

1. **Customize credentials**: Update `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`
2. **Add more fields**: Extend the models in `db/models.py`
3. **Implement file uploads**: Add image/audio upload handlers
4. **Add more validation**: Extend Pydantic models in `crud.py`
5. **Deploy**: Use a production ASGI server like Gunicorn
