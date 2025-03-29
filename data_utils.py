import pandas as pd
import numpy as np

def load_and_prepare_data():
    """
    Load the library circulation data and prepare it for analysis.
    """
    # Update file path to match your actual data file
    file_path = 'data/Daily Circulation Report-reportresults_Jan 2024_June 2024.xls - Sheet1.csv'
    df = pd.read_csv(file_path)
    
    # Convert date to datetime
# Convert date to datetime - ADD THIS LINE FIRST
    df['Date'] = pd.to_datetime(df['Date'])

    # Then extract datetime components
    df['Hour'] = df['Date'].dt.hour
    df['Day'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    df['Week'] = df['Date'].dt.isocalendar().week
    
    # Filter for checkout transactions
# Filter for checkout transactions
    checkouts = df[df['Transaction'].str.contains('Check out', case=False, na=False)]

# Add this line
    checkouts['Subject'] = checkouts['Title'].apply(categorize_book)

    return df, checkouts

def categorize_book(title):
    """
    Categorize books into subjects based on keywords in titles.
    
    Args:
        title: Book title string
        
    Returns:
        category: Subject category string
    """
    if pd.isna(title):
        return "Unknown"
    
    title = str(title).lower()
    
    # Define categories based on keywords
    categories = {
        "Computer Science & Programming": ['programming', 'python', 'c++', 'java', 'computer', 'data structure', 
                                          'algorithm', 'database', 'software', 'network', 'digital', 'operating system',
                                          'ai', 'machine learning', 'artificial intelligence'],
        "Mathematics": ['mathematics', 'calculus', 'algebra', 'linear', 'statistic', 'discrete', 'engineering mathematics',
                       'laplace', 'differential'],
        "Engineering": ['engineering', 'mechanical', 'electrical', 'civil', 'electronic', 'circuit', 'machine element', 
                       'manufacturing', 'fluid', 'thermodynamics', 'cad', 'cam', 'control system', 'hydraulic', 'drawing'],
        "Physics": ['physics', 'optics', 'semiconductor', 'mechanics'],
        "Chemistry": ['chemistry', 'organic', 'engineering chemistry'],
        "Biology & Biotechnology": ['biology', 'biotechnology', 'microbiology', 'biochemistry', 'immunology'],
        "Management & Business": ['management', 'business', 'analytics', 'entrepreneurship', 'economics', 'project management',
                                 'marketing', 'sales'],
        "Constitution & Ethics": ['constitution', 'ethics', 'human rights', 'professional ethics'],
        "Design & Architecture": ['design', 'architecture', 'drawing', 'planning', 'town planning', 'urban', 'buildings'],
        "Communication Skills": ['communication', 'language', 'english', 'kannada', 'kali']
    }
    
    for category, keywords in categories.items():
        if any(keyword in title for keyword in keywords):
            return category
    
    return "Other"