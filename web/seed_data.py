#!/usr/bin/env python3
"""
Sample data seeder for the Tourism Bot admin panel.
Run this script to populate the database with sample cities, excursions, and points.
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import AsyncSessionLocal
from db.models import City, Excursion, Point

async def seed_database():
    """Populate the database with sample data"""
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        existing_cities = await session.execute("SELECT COUNT(*) FROM cities")
        if existing_cities.scalar() > 0:
            print("Database already contains data. Skipping seed.")
            return

        # Create sample cities
        cities_data = [
            {"name": "Paris"},
            {"name": "London"},
            {"name": "New York"},
            {"name": "Tokyo"}
        ]
        
        cities = []
        for city_data in cities_data:
            city = City(**city_data)
            session.add(city)
            cities.append(city)
        
        await session.flush()  # Get IDs for cities
        
        # Create sample excursions
        excursions_data = [
            {
                "city_id": cities[0].id,  # Paris
                "title": "Historic Paris Walking Tour",
                "description": "Explore the historic heart of Paris, visiting iconic landmarks and hidden gems."
            },
            {
                "city_id": cities[0].id,  # Paris
                "title": "Art and Culture Tour",
                "description": "Discover Paris's rich artistic heritage through museums and galleries."
            },
            {
                "city_id": cities[1].id,  # London
                "title": "Royal London Experience",
                "description": "Visit the royal palaces and learn about British monarchy history."
            },
            {
                "city_id": cities[2].id,  # New York
                "title": "Manhattan Highlights",
                "description": "See the best of Manhattan including Central Park, Times Square, and more."
            }
        ]
        
        excursions = []
        for excursion_data in excursions_data:
            excursion = Excursion(**excursion_data)
            session.add(excursion)
            excursions.append(excursion)
        
        await session.flush()  # Get IDs for excursions
        
        # Create sample points
        points_data = [
            # Paris Historic Tour Points
            {
                "excursion_id": excursions[0].id,
                "order": 1,
                "title": "Notre-Dame Cathedral",
                "text": "Gothic masterpiece and symbol of Paris. Learn about its history and architecture.",
                "lat": 48.8530,
                "lng": 2.3499,
                "audio": "media/audio/notre_dame.mp3",
                "image": "media/images/notre_dame.jpg"
            },
            {
                "excursion_id": excursions[0].id,
                "order": 2,
                "title": "Sainte-Chapelle",
                "text": "Marvel at the stunning stained glass windows of this royal chapel.",
                "lat": 48.8555,
                "lng": 2.3452,
                "audio": "media/audio/sainte_chapelle.mp3",
                "image": "media/images/sainte_chapelle.jpg"
            },
            # London Royal Tour Points
            {
                "excursion_id": excursions[2].id,
                "order": 1,
                "title": "Buckingham Palace",
                "text": "The official residence of the British monarch. Watch the Changing of the Guard ceremony.",
                "lat": 51.5014,
                "lng": -0.1419,
                "audio": "media/audio/buckingham_palace.mp3",
                "image": "media/images/buckingham_palace.jpg"
            },
            {
                "excursion_id": excursions[2].id,
                "order": 2,
                "title": "Westminster Abbey",
                "text": "Historic church where British monarchs are crowned and buried.",
                "lat": 51.4994,
                "lng": -0.1273,
                "audio": "media/audio/westminster_abbey.mp3",
                "image": "media/images/westminster_abbey.jpg"
            }
        ]
        
        for point_data in points_data:
            point = Point(**point_data)
            session.add(point)
        
        await session.commit()
        print("✅ Database seeded successfully!")
        print(f"Created {len(cities)} cities, {len(excursions)} excursions, and {len(points_data)} points.")

if __name__ == "__main__":
    print("🌱 Seeding database with sample data...")
    asyncio.run(seed_database())