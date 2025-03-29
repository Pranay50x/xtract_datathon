import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter, defaultdict
from data_utils import load_and_prepare_data

# Create directories for plots
os.makedirs('plots/reading_journeys', exist_ok=True)

# Load data
df, checkouts = load_and_prepare_data()

def analyze_reading_journeys():
    # Track patron reading sequences
    patron_sequences = defaultdict(list)
    
    # Group by patron ID (2nd column in data) and sort by date
    for patron_id in df.iloc[:, 1].unique():
        patron_df = df[df.iloc[:, 1] == patron_id].sort_values('Date')
        # Only include checkout transactions
        checkout_df = patron_df[patron_df['Transaction'] == 'Check out']
        
        if len(checkout_df) > 1:  # Only consider patrons with multiple checkouts
            subjects = checkout_df['Subject'].tolist()
            patron_sequences[patron_id] = subjects
    
    # Analyze transitions between subjects
    transitions = defaultdict(Counter)
    for patron, sequence in patron_sequences.items():
        for i in range(len(sequence)-1):
            from_subject = sequence[i]
            to_subject = sequence[i+1]
            transitions[from_subject][to_subject] += 1
    
    # Get top subjects for visualization
    all_subjects = df['Subject'].unique()
    subject_counts = df[df['Transaction'] == 'Check out']['Subject'].value_counts()
    top_subjects = subject_counts.nlargest(8).index.tolist()
    
    # Create transition matrix
    transition_matrix = pd.DataFrame(0, index=top_subjects, columns=top_subjects)
    for from_subj in top_subjects:
        for to_subj in top_subjects:
            if from_subj in transitions and to_subj in transitions[from_subj]:
                transition_matrix.loc[from_subj, to_subj] = transitions[from_subj][to_subj]
    
    # Plot transition heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(transition_matrix, annot=True, cmap='YlGnBu', fmt='d')
    plt.title('Reading Journey Transitions Between Subjects')
    plt.tight_layout()
    plt.savefig('plots/reading_journeys/transition_heatmap.png', dpi=300)
    plt.close()
    
    # Calculate transition probabilities
    prob_matrix = transition_matrix.copy()
    for i, row in prob_matrix.iterrows():
        row_sum = row.sum()
        if row_sum > 0:
            prob_matrix.loc[i] = row / row_sum
    
    # Plot probability heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(prob_matrix, annot=True, cmap='YlGnBu', fmt='.2f')
    plt.title('Reading Journey Transition Probabilities')
    plt.tight_layout()
    plt.savefig('plots/reading_journeys/transition_probabilities.png', dpi=300)
    plt.close()
    
    # Identify common reading paths (sequences of 3 or more subjects)
    reading_paths = []
    for patron, sequence in patron_sequences.items():
        if len(sequence) >= 3:
            for i in range(len(sequence)-2):
                path = (sequence[i], sequence[i+1], sequence[i+2])
                reading_paths.append(path)
    
    path_counter = Counter(reading_paths)
    common_paths = path_counter.most_common(10)
    
    # Plot common reading paths
    path_labels = [' → '.join(path) for path, count in common_paths]
    path_counts = [count for path, count in common_paths]
    
    plt.figure(figsize=(14, 8))
    plt.barh(path_labels, path_counts, color='teal')
    plt.xlabel('Frequency')
    plt.ylabel('Reading Path')
    plt.title('Most Common Reading Paths (3-Subject Sequences)')
    plt.tight_layout()
    plt.savefig('plots/reading_journeys/common_paths.png', dpi=300)
    plt.close()
    
    return transitions, transition_matrix, common_paths

if __name__ == "__main__":
    transitions, transition_matrix, common_paths = analyze_reading_journeys()
    print("Reading journey analysis complete. Plots saved to plots/reading_journeys/")