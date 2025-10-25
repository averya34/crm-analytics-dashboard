# CRM Analytics Dashboard - Documentation

## Overview
Professional CRM analytics dashboard built with Streamlit for real-time lead tracking and performance monitoring.

## Features
- **Overview Dashboard**: Key metrics, conversion rates, lead trends
- **Appointments**: Scheduling analysis and completion tracking
- **Agent Performance**: Individual and team metrics
- **Lead Sources**: ROI and conversion by channel
- **Tag Analysis**: Lead categorization insights

## Deployment

### Quick Deploy
1. Visit https://share.streamlit.io/
2. Connect repository: averya34/crm-analytics-dashboard
3. Main file: streamlit_app.py
4. Deploy

### Configuration
Add Google Drive credentials in Streamlit Cloud Settings > Secrets:
```toml
[google_drive]
type = "service_account"
project_id = "your-project-id"
private_key = "your-private-key"
client_email = "your-email@project.iam.gserviceaccount.com"
```

## Data Requirements
Required columns: Name, Email, Phone, Date Added, Stage, Source, Agent

Optional: Tags, Is Contacted, Notes

## Monitoring
- GitHub Actions CI/CD validates code on every push
- Data validation runs automatically on upload
- Error logging in Streamlit Cloud logs

## Support
- Repository: https://github.com/averya34/crm-analytics-dashboard
- Issues: https://github.com/averya34/crm-analytics-dashboard/issues
