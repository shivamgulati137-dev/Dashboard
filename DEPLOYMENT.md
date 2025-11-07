# Deployment Guide

This guide provides step-by-step instructions for deploying the Urban Svamitva Dashboard.

## Pre-Deployment Checklist

- [ ] All dependencies are listed in `requirements.txt`
- [ ] CSV data files are included or will be created on first run
- [ ] `.gitignore` is configured properly
- [ ] README.md is updated with current features
- [ ] Code is tested locally

## Deployment Options

### 1. Streamlit Cloud (Easiest - Recommended)

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select repository and branch
6. Set main file: `app.py`
7. Click "Deploy"

**Advantages:**
- Free tier available
- Automatic deployments on git push
- Persistent storage for CSV files
- Easy to use

### 2. Heroku

**Prerequisites:**
- Heroku CLI installed
- Git repository initialized

**Steps:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set Python version (optional)
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open app
heroku open
```

**Note:** Make sure `Procfile` and `runtime.txt` are in your repository.

### 3. Docker

**Build and run:**
```bash
# Build image
docker build -t svamitva-dashboard .

# Run container
docker run -p 8501:8501 svamitva-dashboard
```

**For production:**
```bash
# Run with volume for data persistence
docker run -d -p 8501:8501 -v $(pwd)/data:/app/data svamitva-dashboard
```

### 4. AWS EC2

**Steps:**
1. Launch EC2 instance (Ubuntu recommended)
2. SSH into instance
3. Install Python and pip
4. Clone repository
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
7. Configure security group to allow port 8501
8. Use screen or systemd to run in background

### 5. Railway

**Steps:**
1. Sign up at [railway.app](https://railway.app)
2. Create new project
3. Connect GitHub repository
4. Railway will auto-detect Python
5. Set start command: `streamlit run app.py --server.port=$PORT`
6. Deploy

### 6. Render

**Steps:**
1. Sign up at [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy

## Environment Variables

If needed, you can set environment variables for:
- Port number
- Data file paths
- API keys (if added later)

## Data Persistence

**Important:** CSV files are stored in the application directory. For production:

1. **Streamlit Cloud:** Files persist automatically
2. **Heroku:** Use Heroku Postgres or external storage (S3, etc.)
3. **Docker:** Use volumes for data persistence
4. **Cloud Platforms:** Consider using cloud storage (S3, GCS, Azure Blob)

## Security Considerations

1. **Authentication:** Consider adding Streamlit authentication
2. **HTTPS:** Use HTTPS in production
3. **Secrets:** Store sensitive data in environment variables
4. **File Permissions:** Ensure proper file permissions

## Monitoring

Consider adding:
- Application monitoring (Sentry, etc.)
- Logging
- Error tracking
- Usage analytics

## Backup Strategy

1. Regular backups of CSV files
2. Version control for data files
3. Automated backups to cloud storage

## Troubleshooting

### Port Issues
- Ensure port is correctly configured
- Check firewall settings
- Verify security groups (cloud platforms)

### Data Not Persisting
- Check file permissions
- Verify write access
- Use volumes (Docker) or external storage

### Import Errors
- Verify all dependencies in requirements.txt
- Check Python version compatibility
- Ensure all packages are installed

## Support

For deployment issues, refer to:
- Streamlit documentation: https://docs.streamlit.io
- Platform-specific documentation
- README.md in this repository

