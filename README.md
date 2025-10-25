# CRM Analytics Dashboard

A dynamic Streamlit dashboard for Follow Up Boss CRM data analysis.

## Features

- **Overview Dashboard**: Total leads, contact rates, appointment metrics
- **Appointment Analytics**: Timeline and completion tracking
- **Agent Performance**: Individual agent statistics and comparisons
- **Source Analysis**: Lead source breakdown and performance
- **Tag Segmentation**: Campaign and buyer type analysis

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `streamlit run streamlit_app.py`

## Deployment

Deploy to Streamlit Cloud:
1. Connect your GitHub repository
2. Set main file path: `streamlit_app.py`
3. Deploy

## Data Integration

Currently uses sample data. To connect to Google Drive:
1. Set up Google Cloud project with Drive API enabled
2. Add OAuth credentials
3. Update data loading function in `streamlit_app.py`

## Built With

- Streamlit
- Pandas
- Plotly
- Google Drive API
