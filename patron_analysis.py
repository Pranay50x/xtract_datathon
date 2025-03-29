import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from data_utils import load_and_prepare_data

# Create directories for plots
os.makedirs('plots/patron_analysis', exist_ok=True)

# Load data
df, checkouts = load_and_prepare_data()

def analyze_patron_patterns():
    # Department analysis
    # For department, use 3rd column in the data
    dept_interests = checkouts.groupby([df.iloc[:, 3], 'Subject']).size().unstack().fillna(0)
    
    # Get top departments by activity
    top_depts = dept_interests.sum(axis=1).nlargest(8).index
    dept_interests_top = dept_interests.loc[top_depts]
    
    # Plot department interests
    plt.figure(figsize=(14, 10))
    dept_interests_top.plot(kind='bar', stacked=True)
    plt.title('Subject Preferences by Department')
    plt.xlabel('Department')
    plt.ylabel('Number of Checkouts')
    plt.legend(title='Subject', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/patron_analysis/department_interests.png', dpi=300)
    plt.close()
    
    # User type analysis (UG, PG, ST, etc.)
    # For user type, use 4th column in the data
    user_interests = checkouts.groupby([df.iloc[:, 4], 'Subject']).size().unstack().fillna(0)
    
    plt.figure(figsize=(14, 8))
    user_interests.plot(kind='bar', stacked=True)
    plt.title('Subject Preferences by User Type')
    plt.xlabel('User Type')
    plt.ylabel('Number of Checkouts')
    plt.legend(title='Subject', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/patron_analysis/user_type_interests.png', dpi=300)
    plt.close()
    
    # Reading diversity by department
    # Calculate number of unique subjects per department
    dept_diversity = checkouts.groupby(df.iloc[:, 3])['Subject'].nunique().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    dept_diversity.plot(kind='bar', color='purple')
    plt.title('Reading Diversity by Department')
    plt.xlabel('Department')
    plt.ylabel('Number of Different Subjects')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('plots/patron_analysis/department_diversity.png', dpi=300)
    plt.close()
    
    return dept_interests, user_interests, dept_diversity

if __name__ == "__main__":
    dept_interests, user_interests, dept_diversity = analyze_patron_patterns()
    print("Patron analysis complete. Plots saved to plots/patron_analysis/")