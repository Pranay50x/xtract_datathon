import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter, defaultdict
from sklearn.cluster import KMeans
from data_utils import load_and_prepare_data

# Create directories for plots
os.makedirs('plots/community_engagement', exist_ok=True)

# Load data
df, checkouts = load_and_prepare_data()

def analyze_community_engagement():
    # Identify optimal event times
    df['Hour'] = df['Date'].dt.hour
    df['Day'] = df['Date'].dt.day_name()
    
    # Peak activity times
    activity_by_hour_day = df.groupby(['Day', 'Hour']).size().unstack().fillna(0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    activity_by_hour_day = activity_by_hour_day.reindex(day_order)
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(activity_by_hour_day, cmap='viridis', annot=True, fmt='g')
    plt.title('Best Times for Community Events (Based on Library Activity)')
    plt.tight_layout()
    plt.savefig('plots/community_engagement/optimal_event_times.png', dpi=300)
    plt.close()
    
    # Identify potential book club topics based on popular subject combinations
    # Create a patron-subject matrix
    patron_subjects = defaultdict(Counter)
    
    for _, row in checkouts.iterrows():
        patron_id = row.iloc[1]  # Patron ID is in 2nd column
        subject = row['Subject']
        patron_subjects[patron_id][subject] += 1
    
    # Find subjects that are frequently borrowed together
    subject_combinations = Counter()
    
    for patron, subjects in patron_subjects.items():
        subject_list = list(subjects.keys())
        if len(subject_list) >= 2:
            for i in range(len(subject_list)):
                for j in range(i+1, len(subject_list)):
                    # Sort to ensure consistent ordering
                    combination = tuple(sorted([subject_list[i], subject_list[j]]))
                    subject_combinations[combination] += 1
    
    # Plot top subject combinations
    top_combinations = subject_combinations.most_common(10)
    combination_labels = [' & '.join(combo) for combo, _ in top_combinations]
    combination_counts = [count for _, count in top_combinations]
    
    plt.figure(figsize=(14, 8))
    plt.barh(combination_labels, combination_counts, color='orange')
    plt.xlabel('Frequency')
    plt.ylabel('Subject Combination')
    plt.title('Potential Book Club Topics (Popular Subject Combinations)')
    plt.tight_layout()
    plt.savefig('plots/community_engagement/book_club_topics.png', dpi=300)
    plt.close()
    
    # Identify underserved subjects (low activity relative to collection size)
    # This would need collection size data, but we can approximate with a random distribution
    # For real analysis, you'd compare checkout frequency to collection size
    
    subject_checkouts = checkouts['Subject'].value_counts()
    total_checkouts = subject_checkouts.sum()
    
    # Calculate expected checkout distribution if all subjects were equally popular
    # (This is just an illustration - real analysis would use collection size)
    num_subjects = len(subject_checkouts)
    expected_checkouts = pd.Series([total_checkouts/num_subjects] * num_subjects, index=subject_checkouts.index)
    
    # Calculate ratio of actual to expected
    utilization_ratio = subject_checkouts / expected_checkouts
    
    plt.figure(figsize=(14, 8))
    utilization_ratio.sort_values().plot(kind='bar', color='lightblue')
    plt.axhline(y=1, color='red', linestyle='--')
    plt.title('Subject Utilization Ratio (Actual vs. Expected Checkouts)')
    plt.xlabel('Subject')
    plt.ylabel('Utilization Ratio')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('plots/community_engagement/subject_utilization.png', dpi=300)
    plt.close()
    
    return activity_by_hour_day, top_combinations, utilization_ratio

if __name__ == "__main__":
    activity_by_hour_day, top_combinations, utilization_ratio = analyze_community_engagement()
    print("Community engagement analysis complete. Plots saved to plots/community_engagement/")