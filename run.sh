#!/bin/bash

echo "🚀 Starting Topiq..."

# Activate virtual environment
source myenv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found! Copy .env.example to .env and fill in your values."
    exit 1
fi

# Install/update dependencies
pip install -r requirements.txt -q

# Create logs directory
mkdir -p logs

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --run-syncdb

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput -v 0

# Seed data if DB is empty
echo "🌱 Checking seed data..."
python manage.py seed_data

# Start server
echo "✅ Server starting at http://127.0.0.1:8090/"
python manage.py runserver 0.0.0.0:8090
