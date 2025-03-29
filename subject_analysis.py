import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from data_utils import load_and_prepare_data, categorize_book

# Create directories for plots
os.makedirs('plots/subject_popularity', exist_ok=True)

# Load data
df, checkouts = load_and_prepare_data()

# Overall subject popularity
def analyze_subject_popularity():
    # Subject popularity by month
    subjects_by_month = checkouts.groupby([pd.Grouper(key='Date', freq='ME'), 'Subject']).size().unstack().fillna(0)
    
    # Plot monthly trends
    plt.figure(figsize=(14, 8))
    subjects_by_month = checkouts.groupby([pd.Grouper(key='Date', freq='ME'), 'Subject']).size().unstack().fillna(0)

    plt.title('Subject Popularity by Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Checkouts')
    plt.xticks(rotation=45)
    plt.legend(title='Subject', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/subject_popularity/monthly_trends.png', dpi=300)
    plt.close()
    
    # Top subjects overall
    top_subjects = subjects_by_month.sum().sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    top_subjects.plot(kind='bar', color='skyblue')
    plt.title('Subjects by Popularity')
    plt.xlabel('Subject')
    plt.ylabel('Total Checkouts')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('plots/subject_popularity/overall_ranking.png', dpi=300)
    plt.close()
    
    # Subject popularity by day of week
    df['Day'] = df['Date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_checkouts = checkouts.groupby(['Day', 'Subject']).size().unstack().fillna(0)
    daily_checkouts = daily_checkouts.reindex(day_order)
    
    plt.figure(figsize=(14, 8))
    daily_checkouts.plot(kind='bar', stacked=True)
    plt.title('Subject Popularity by Day of Week')
    plt.xlabel('Day')
    plt.ylabel('Number of Checkouts')
    plt.legend(title='Subject', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/subject_popularity/day_of_week.png', dpi=300)
    plt.close()
    
    return subjects_by_month, top_subjects, daily_checkouts

if __name__ == "__main__":
    subjects_by_month, top_subjects, daily_checkouts = analyze_subject_popularity()
    print("Subject popularity analysis complete. Plots saved to plots/subject_popularity/")