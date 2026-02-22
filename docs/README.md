# Tourism Bot Admin Panel

A user-friendly web interface for managing cities, excursions, and points of interest for the Tourism Bot.

## Features

- 🏙️ **City Management**: Add, edit, delete, and search cities
- 🗺️ **Excursion Management**: Create detailed excursions with descriptions
- 📍 **Point Management**: Manage excursion points with coordinates, audio, and images
- 🔍 **Search & Filter**: Search and sort all data easily
- ✅ **Form Validation**: Built-in validation for all fields
- 🔐 **Authentication**: Secure admin login
- 📱 **Responsive Design**: Works on desktop and mobile

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables (Optional)
Create a `.env` file or set environment variables:
```bash
# Database URL (default: sqlite:///./db.sqlite3)
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3

# Admin credentials (defaults shown)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 3. Start the Admin Panel
```bash
python web/run_admin.py
```

Or manually:
```bash
uvicorn web.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Admin Panel
- Open your browser and go to: http://localhost:8000/admin
- Login with credentials: `admin` / `admin123` (or your custom credentials)

### 5. Seed Sample Data (Optional)
To populate the database with sample data for testing:
```bash
python web/seed_data.py
```

## Admin Panel Usage

### Managing Cities
1. Go to **Cities** section
2. Click **Create** to add a new city
3. Fill in the city name (2-100 characters)
4. Save to create the city

### Managing Excursions
1. Go to **Excursions** section
2. Click **Create** to add a new excursion
3. Select a city from the dropdown
4. Enter title (5-200 characters) and description (10-2000 characters)
5. Save to create the excursion

### Managing Points
1. Go to **Excursion Points** section
2. Click **Create** to add a new point
3. Fill in the required fields:
   - **Excursion**: Select from dropdown
   - **Order**: Sequence number (1-100)
   - **Title**: Point name (3-200 characters)
   - **Text**: Detailed description (10-2000 characters)
   - **Latitude**: GPS coordinate (-90 to 90)
   - **Longitude**: GPS coordinate (-180 to 180)
   - **Audio**: Optional audio file path (e.g., `media/audio/point1.mp3`)
   - **Image**: Optional image file path (e.g., `media/images/point1.jpg`)

## Form Validation

The admin panel includes comprehensive validation:
- **Required fields**: Cannot be empty
- **Length limits**: Minimum and maximum character counts
- **Number ranges**: Coordinates within valid GPS ranges
- **Order validation**: Ensures proper sequencing of points

## Search and Filtering

- **Search**: Use the search box to find cities, excursions, or points by name/title
- **Sort**: Click column headers to sort data
- **Filter**: Use the built-in filters for better data management

## Security Notes

- Change default admin credentials in production
- Use environment variables for sensitive configuration
- The admin panel is protected by session-based authentication
- Consider using HTTPS in production environments

## File Structure

```
web/
├── admin.py          # Admin model configurations
├── auth.py           # Authentication backend
├── main.py           # FastAPI application
├── run_admin.py      # Startup script
└── seed_data.py      # Sample data seeder
```

## Troubleshooting

### Database Issues
- Ensure the database file is writable
- Check DATABASE_URL in your environment
- Run the health check: http://localhost:8000/health

### Authentication Issues
- Verify ADMIN_USERNAME and ADMIN_PASSWORD
- Clear browser cookies if login fails
- Check server logs for authentication errors

### Form Validation Errors
- Check field requirements and limits
- Ensure coordinates are in valid ranges
- Verify file paths for audio/image fields

## API Endpoints

- `/admin` - Admin panel interface
- `/health` - Health check endpoint
- `/` - Redirects to admin panel

## Development

To modify the admin interface:
1. Edit `web/admin.py` for model configurations
2. Update `web/main.py` for application settings
3. Modify `web/auth.py` for authentication logic

The admin panel uses SQLAdmin with FastAPI for a modern, responsive interface.