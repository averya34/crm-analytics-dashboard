import pandas as pd
from datetime import datetime

def validate_crm_data(df):
    """Validate CRM data structure and content"""
    required_columns = ['Name', 'Email', 'Phone', 'Date Added', 'Stage', 'Source', 'Agent']
    errors = []
    
    # Check required columns
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        errors.append('Missing columns: ' + ', '.join(missing))
    
    # Validate email format
    if 'Email' in df.columns:
        invalid_emails = df[~df['Email'].str.contains('@', na=False)]
        if len(invalid_emails) > 0:
            errors.append(str(len(invalid_emails)) + ' invalid email addresses')
    
    # Validate dates
    if 'Date Added' in df.columns:
        try:
            pd.to_datetime(df['Date Added'])
        except:
            errors.append('Invalid date format in Date Added')
    
    return {'valid': len(errors) == 0, 'errors': errors, 'row_count': len(df)}

def clean_crm_data(df):
    """Clean and standardize CRM data"""
    df = df.copy()
    
    # Strip whitespace
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    # Standardize dates
    if 'Date Added' in df.columns:
        df['Date Added'] = pd.to_datetime(df['Date Added'], errors='coerce')
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['Email'], keep='first')
    
    return df
