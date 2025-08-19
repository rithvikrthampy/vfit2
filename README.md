# Virtual Try-On System

## Project Structure

```
vfit2/
├── backend/                 # Django backend
│   ├── server/             # Django project settings
│   ├── viewer/             # Main application views
│   ├── pix2surf/           # AI processing engine
│   └── data/               # Generated media files
├── frontend/               # Frontend templates and static files
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, assets
├── tools/                  # External tools and dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml     # Docker Compose setup
└── environment.yml         # Conda environment specification
```

## API Endpoints

- `GET /` - Main gallery page
- `GET /api/shirts/` - List available shirts
- `GET /api/run/` - Process virtual try-on (with img_id, pose_id, low_type parameters)
- `GET /viewer/` - 3D model viewer page

## How to Run

### Local Development

```bash
# Set up conda environment
conda env create -f environment.yml
conda activate pix2surf_py39

# Start the development server
cd backend
python manage.py runserver
```

### Docker Deployment

```bash
# Quick start with Docker Compose
docker-compose up --build

# Access at http://localhost:8000
```