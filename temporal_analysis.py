import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from data_utils import load_and_prepare_data

# Create directories for plots
os.makedirs('plots/temporal_patterns', exist_ok=True)

# Load data
df, checkouts = load_and_prepare_data()

def analyze_temporal_patterns():
    # Extract time components
    df['Hour'] = df['Date'].dt.hour
    df['Day'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    df['Week'] = df['Date'].dt.isocalendar().week
    
    # Time of day patterns
    checkouts['Hour'] = checkouts['Date'].dt.hour
    checkouts['Day'] = checkouts['Date'].dt.day_name()
    checkouts['Month'] = checkouts['Date'].dt.month_name()
    checkouts['Week'] = checkouts['Date'].dt.isocalendar().week
    
    plt.figure(figsize=(14, 8))
    hourly_checkouts.plot(kind='line', marker='o')
    plt.title('Subject Popularity by Hour of Day')
    plt.xlabel('Hour (24-hour format)')
    plt.ylabel('Number of Checkouts')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Subject', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/temporal_patterns/hourly_trends.png', dpi=300)
    plt.close()
    
    # Monthly patterns
    monthly_checkouts = checkouts.groupby(['Month', 'Subject']).size().unstack().fillna(0)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June']
    monthly_checkouts = monthly_checkouts.reindex(month_order)
    
    plt.figure(figsize=(14, 8))
    monthly_checkouts.plot(kind='line', marker='o')
    plt.title('Subject Popularity by Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Checkouts')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Subject', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/temporal_patterns/monthly_trends.png', dpi=300)
    plt.close()
    
    # Weekly patterns
    weekly_checkouts = checkouts.groupby(['Week', 'Subject']).size().unstack().fillna(0)
    
    plt.figure(figsize=(16, 8))
    weekly_checkouts.plot(kind='line', marker='o')
    plt.title('Subject Popularity by Week')
    plt.xlabel('Week of Year')
    plt.ylabel('Number of Checkouts')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Subject', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/temporal_patterns/weekly_trends.png', dpi=300)
    plt.close()
    
    # Heat map of day and hour
    day_hour_checkouts = checkouts.groupby(['Day', 'Hour']).size().unstack().fillna(0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_hour_checkouts = day_hour_checkouts.reindex(day_order)
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(day_hour_checkouts, cmap='YlGnBu', annot=True, fmt='g')
    plt.title('Checkout Activity by Day and Hour')
    plt.tight_layout()
    plt.savefig('plots/temporal_patterns/day_hour_heatmap.png', dpi=300)
    plt.close()
    
    return hourly_checkouts, monthly_checkouts, weekly_checkouts, day_hour_checkouts

if __name__ == "__main__":
    hourly_checkouts, monthly_checkouts, weekly_checkouts, day_hour_checkouts = analyze_temporal_patterns()
    print("Temporal pattern analysis complete. Plots saved to plots/temporal_patterns/")