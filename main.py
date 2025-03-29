import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict

# Create all plot directories
for directory in ['plots', 'plots/subject_popularity', 'plots/reading_journeys', 
                 'plots/patron_analysis', 'plots/temporal_patterns', 
                 'plots/community_engagement']:
    os.makedirs(directory, exist_ok=True)

# Import and run all analyses
from subject_analysis import analyze_subject_popularity
from reading_journey import analyze_reading_journeys
from patron_analysis import analyze_patron_patterns
from temporal_analysis import analyze_temporal_patterns
from community_engagement import analyze_community_engagement

def run_all_analyses():
    print("Starting comprehensive library circulation analysis...")
    
    print("\n1. Analyzing subject popularity...")
    subjects_by_month, top_subjects, daily_checkouts = analyze_subject_popularity()
    
    print("\n2. Analyzing reading journeys...")
    transitions, transition_matrix, common_paths = analyze_reading_journeys()
    
    print("\n3. Analyzing patron patterns...")
    dept_interests, user_interests, dept_diversity = analyze_patron_patterns()
    
    print("\n4. Analyzing temporal patterns...")
    hourly_checkouts, monthly_checkouts, weekly_checkouts, day_hour_checkouts = analyze_temporal_patterns()
    
    print("\n5. Analyzing community engagement opportunities...")
    activity_by_hour_day, top_combinations, utilization_ratio = analyze_community_engagement()
    
    print("\nAll analyses complete! Results saved to 'plots' directory.")
    
    # Generate final report with key insights
    generate_insights_summary(top_subjects, transition_matrix, common_paths, 
                             dept_interests, top_combinations, activity_by_hour_day)

def generate_insights_summary(top_subjects, transition_matrix, common_paths, 
                             dept_interests, top_combinations, activity_by_hour_day):
    """Generate a text file with key insights from the analysis"""
    with open('reading_journeys_insights.txt', 'w') as f:
        f.write("LIBRARY READING JOURNEYS & COMMUNITY ENGAGEMENT INSIGHTS\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("1. MOST POPULAR SUBJECTS\n")
        f.write("-" * 30 + "\n")
        for subject, count in top_subjects.head(5).items():
            f.write(f"- {subject}: {count} checkouts\n")
        
        f.write("\n2. TOP READING TRANSITIONS\n")
        f.write("-" * 30 + "\n")
        for from_subj in transition_matrix.index:
            top_transition = transition_matrix.loc[from_subj].nlargest(1)
            if top_transition.values[0] > 0:
                to_subj = top_transition.index[0]
                f.write(f"- {from_subj} → {to_subj}: {top_transition.values[0]} transitions\n")
        
        f.write("\n3. COMMON READING PATHS\n")
        f.write("-" * 30 + "\n")
        for path, count in common_paths[:5]:
            f.write(f"- {' → '.join(path)}: {count} occurrences\n")
        
        f.write("\n4. DEPARTMENT READING PREFERENCES\n")
        f.write("-" * 30 + "\n")
        for dept in dept_interests.index[:5]:
            top_subject = dept_interests.loc[dept].idxmax()
            f.write(f"- {dept}: Prefers {top_subject}\n")
        
        f.write("\n5. POTENTIAL BOOK CLUB TOPICS\n")
        f.write("-" * 30 + "\n")
        for combo, count in top_combinations[:5]:
            f.write(f"- {' & '.join(combo)}: {count} co-occurrences\n")
        
        f.write("\n6. OPTIMAL EVENT TIMES\n")
        f.write("-" * 30 + "\n")
        best_day = activity_by_hour_day.sum(axis=1).idxmax()
        best_hour = activity_by_hour_day.sum().idxmax()
        best_day_hour = activity_by_hour_day.stack().idxmax()
        f.write(f"- Busiest day: {best_day}\n")
        f.write(f"- Busiest hour: {best_hour}:00\n")
        f.write(f"- Peak activity time: {best_day_hour[0]} at {best_day_hour[1]}:00\n")
        
        f.write("\n7. COMMUNITY ENGAGEMENT RECOMMENDATIONS\n")
        f.write("-" * 30 + "\n")
        f.write("a) Reading Path Programs:\n")
        for path, _ in common_paths[:3]:
            f.write(f"   - '{' → '.join(path)}' themed reading challenge\n")
        
        f.write("\nb) Book Clubs:\n")
        for combo, _ in top_combinations[:3]:
            f.write(f"   - '{' & '.join(combo)}' discussion group\n")
        
        f.write("\nc) Department-Specific Initiatives:\n")
        top_3_depts = dept_interests.sum(axis=1).nlargest(3).index
        for dept in top_3_depts:
            top_subject = dept_interests.loc[dept].idxmax()
            f.write(f"   - {dept}: {top_subject} workshop or seminar\n")
        
        f.write("\n\nAnalysis completed on March 29, 2025\n")
    
    print(f"Key insights saved to 'reading_journeys_insights.txt'")
if __name__ == "__main__":
    run_all_analyses()