# Urban Svamitva Scheme Dashboard - Ludhiana MCL

A comprehensive Streamlit dashboard for tracking the Urban Svamitva Scheme progress across Ludhiana Municipal Corporation.

**Developed by:** Shivam Gulati (Land Revenue Fellow)

## Features

### 📊 Overview Tab
- Key metrics: Total Villages, Survey Completed, Map 2 awaited, Ground Truthing
- Village Progress Details table with all village information
- Progress bar chart showing villages in each phase
- Municipal zone distribution chart
- Status distribution chart
- Zone vs Status heatmap
- Color-coded status indicators

### 👥 Responsibility Matrix Tab
- Phase-wise responsibility mapping (excluding Notification and Card Issuance)
- Contact directory for Property Tax and ATP/MTP by municipal zone
- One Point of Contact (DC Office) - Shivam Gulati, 62844-12362
- One Point of Contact (MCL) - Nirvaan, ATP HQ, 95927-35111

### 💬 Remarks & Help Required Tab
- Officials can submit remarks and request help from higher officials
- Filter remarks by Department, Status, and Help Type
- Higher officials can respond to remarks
- Export remarks to CSV
- Track status: Pending, In Progress, Resolved, Referred

### 💾 Data Management Tab
- Manual village data update interface
- Bulk CSV upload functionality
- Add new villages
- Update phase progress
- Real-time data saving

## Installation

### Local Development

1. **Clone or download the repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard:**
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Data Structure

The dashboard uses four main CSV files:

1. **villages_data.csv**: Contains village-level data with all phases and dates
2. **progress_data.csv**: Contains phase progress statistics
3. **responsibility_data.csv**: Contains phase-wise responsibility mapping
4. **remarks_data.csv**: Contains remarks and help requests from officials

Sample data files are automatically created on first run if they don't exist.

## Municipal Zones

The dashboard tracks four municipal zones:
- Zone A
- Zone B
- Zone C
- Zone D

## Phase Sequence

1. Notification (DC Administration)
2. Drone Survey Pending (Survey of India)
3. Map 1 awaited (Survey of India)
4. Ground Truthing (Property Tax Dept - HDM/JDM)
5. Map 2 awaited (Survey of India)
6. Pasting (ATP/MTP) - 90 days
7. Objections Hearing (ARRO)
8. Map 3 (Survey of India)
9. Card Issuance (DC Administration)

## Status Indicators

- 🟢 Green: Completed
- 🟡 Yellow: On Track
- 🔴 Red: Behind Schedule

## Deployment

### Streamlit Cloud (Recommended)

1. **Push your code to GitHub**
   - Create a new repository on GitHub
   - Push all files to the repository

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configure data persistence**
   - Streamlit Cloud provides persistent storage
   - CSV files will be saved in the app's file system
   - Data persists across deployments

### Heroku Deployment

1. **Install Heroku CLI** (if not already installed)

2. **Login to Heroku:**
```bash
heroku login
```

3. **Create a Heroku app:**
```bash
heroku create your-app-name
```

4. **Deploy:**
```bash
git push heroku main
```

5. **Open the app:**
```bash
heroku open
```

### Docker Deployment

1. **Build the Docker image:**
```bash
docker build -t svamitva-dashboard .
```

2. **Run the container:**
```bash
docker run -p 8501:8501 svamitva-dashboard
```

### Other Platforms

The dashboard can be deployed on any platform that supports Python and Streamlit:
- AWS EC2
- Google Cloud Platform
- Azure
- DigitalOcean
- Railway
- Render

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Pandas 2.0.0+
- Plotly 5.17.0+
- Openpyxl 3.1.0+
- Python-dateutil 2.8.2+

## File Structure

```
dashboard/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku deployment file
├── setup.sh                    # Setup script for deployment
├── .gitignore                  # Git ignore file
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── villages_data.csv           # Village data
├── progress_data.csv           # Progress statistics
├── responsibility_data.csv     # Responsibility matrix
├── remarks_data.csv            # Remarks and help requests
└── README.md                   # This file
```

## Notes

- Data is automatically saved to CSV files
- The dashboard includes caching for performance
- Export functionality available for CSV format
- All data updates are real-time
- Make sure CSV files are not open in Excel when updating data
- Use the reload button (🔄) in the sidebar to refresh data

## Troubleshooting

### Permission Denied Error
If you get a permission denied error when saving:
1. Close any programs that have the CSV files open (Excel, Notepad, etc.)
2. Check file permissions
3. Make sure you have write access to the directory
4. Try running as administrator if needed

### Data Not Updating
1. Click the reload button (🔄) in the sidebar
2. Clear browser cache
3. Restart the Streamlit app

## Support

For issues or questions, contact:
- **DC Office**: Shivam Gulati, 62844-12362
- **MCL**: Nirvaan, ATP HQ, 95927-35111

## License

This project is developed for Ludhiana Municipal Corporation.
