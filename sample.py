import pandas as pd

# Load your dataset
df = pd.read_csv('data/Rhythm_Restore_Refined.csv')

# Check how many unique target values you have
print("Unique Diet Suggestions:", df['Diet Suggestions'].nunique())
print("Unique Workout Suggestions:", df['Workout Suggestions'].nunique())
print("Unique Sleep Habit Suggestions:", df['Sleep Habit Suggestions'].nunique())
print("Unique Stress Busters:", df['Stress Busters'].nunique())

# Check what are the unique values
print("\nDiet Suggestions Options:", df['Diet Suggestions'].unique())
print("\nWorkout Suggestions Options:", df['Workout Suggestions'].unique())
print("\nSleep Habit Suggestions Options:", df['Sleep Habit Suggestions'].unique())
print("\nStress Busters Options:", df['Stress Busters'].unique())
