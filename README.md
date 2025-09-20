# tasks-app
# 🚀 3-Tier project Management Application

## 📁 Project Structure
```
task-management-app/
├── docker-compose.yml          # Local development
├── docker-compose.prod.yml     # Production overrides
├── init-db.sql                # Database initialization
├── README.md                  # This file
│
├── backend/                   # Python Flask API
│   ├── Dockerfile
│   ├── app.py                # Main application
│   ├── requirements.txt      # Python dependencies
│   └── gunicorn.conf.py      # Production server config
│
├── frontend/                  # NGINX + HTML
│   ├── Dockerfile
│   ├── nginx.conf            # NGINX configuration
│   └── static/
│       ├── index.html        # Frontend application
│       ├── app.js           # JavaScript logic
│       └── styles.css       # Styling
│
└── k8s/                      # Kubernetes manifests
    ├── namespace.yaml
    ├── configmap.yaml
    ├── secrets.yaml
    ├── postgres/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   └── pvc.yaml
    ├── backend/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   └── hpa.yaml
    ├── frontend/
    │   ├── deployment.yaml
    │   └── service.yaml
    ├── ingress.yaml
    └── network-policy.yaml
```

## 🔧 Quick Setup Instructions

### 1. Create Project Directory Structure
```bash
mkdir -p task-management-app/{backend,frontend/static,k8s/{postgres,backend,frontend}}
cd task-management-app
```

### 2. Create Backend Files
```bash
# Create backend directory structure
cd backend/

# Copy the app.py content from the artifacts above
cat > app.py << 'EOF'
[Copy the Fixed Backend App content here]
EOF

# Copy requirements.txt
cat > requirements.txt << 'EOF'
[Copy the Requirements content here]
EOF

# Copy Dockerfile
cat > Dockerfile << 'EOF'
[Copy the Backend Dockerfile content here]
EOF

# Copy Gunicorn config
cat > gunicorn.conf.py << 'EOF'
[Copy the Gunicorn Configuration content here]
EOF

cd ..
```

### 3. Create Frontend Files
```bash
cd frontend/

# Create Dockerfile for NGINX
cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY static/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# Create NGINX config
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    server {
        listen 80;
        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

# Create static files directory
mkdir -p static
# Copy the frontend HTML content from artifacts above into static/index.html

cd ..
```

### 4. Create Database Init Script
```bash
cat > init-db.sql << 'EOF'
-- Database initialization script
CREATE DATABASE taskdb;
CREATE USER taskuser WITH PASSWORD 'taskpass123';
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;
\c taskdb;
GRANT ALL ON SCHEMA public TO taskuser;
EOF
```

### 5. Copy Docker Compose
```bash
# Copy the docker-compose.yml content from artifacts above
```

## 🐳 Running with Docker Compose

### Development Mode
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Access application
# Frontend: http://localhost
# Backend API: http://localhost:5000
# Database: localhost:5432
```

### Production Mode
```bash
# Set environment variables
export POSTGRES_PASSWORD=your-secure-password

# Start with production overrides
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🔍 Testing the Application

### Backend API Tests
```bash
# Health check
curl http://localhost:5000/health

# Add a task
curl -X POST http://localhost:5000/addTask \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Test Description","status":"pending"}'

# List tasks
curl http://localhost:5000/listTasks

# Delete task (replace {id} with actual task ID)
curl -X DELETE http://localhost:5000/deleteTask/{id}
```

### Load Testing for HPA
```bash
# Install hey (HTTP load tester)
go install github.com/rakyll/hey@latest

# Load test
hey -n 1000 -c 50 http://localhost:5000/listTasks
```

## 🚨 Troubleshooting

### Backend Issues
```bash
# Check backend logs
docker-compose logs backend

# Connect to backend container
docker-compose exec backend /bin/sh

# Check database connectivity from backend
docker-compose exec backend python -c "
import psycopg2
conn = psycopg2.connect(host='postgres', database='taskdb', user='taskuser', password='taskpass123')
print('Database connected successfully!')
"
```

### Database Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Connect to database directly
docker-compose exec postgres psql -U taskuser -d taskdb

# Run SQL commands
\l                    # List databases
\dt                   # List tables
SELECT * FROM tasks;  # View all tasks
```

### Performance Tuning
- Adjust worker processes in `gunicorn.conf.py`
- Enable database connection pooling
- Add Redis for caching
- Configure NGINX caching



