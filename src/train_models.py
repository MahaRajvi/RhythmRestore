import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load your dataset
df = pd.read_csv('src/Rhythm_Restore_Refined.csv')

# Rename columns properly
df = df.rename(columns={
    'what time do you usually sleep': 'sleep_time',
    'what time do you usually wake up': 'wake_time',
    'How often do you skip meals?': 'meals_skipped',
    'How would you rate your stress levels during the day?Scale: 1 = No Stress, 5 = Extremely Stressed)': 'stress',
    'Do you feel mentally exhausted before bedtime? ': 'mood',
    'How often are you stuck in traffic?': 'traffic',
    'How much screen time do you get before bed?': 'screen_time'
})

# 🛠 Convert sleep and wake time into sleep_duration_hours
df['sleep_time'] = pd.to_datetime(df['sleep_time'], format='%H:%M:%S', errors='coerce')
df['wake_time'] = pd.to_datetime(df['wake_time'], format='%H:%M:%S', errors='coerce')
# Fix screen_time values: convert '1Hr', '2Hr' -> 1, 2
df['screen_time'] = df['screen_time'].astype(str).str.extract('(\d+)').astype(float)
df['screen_time'] = df['screen_time'].fillna(1.0)  # fallback

df['sleep_duration_hours'] = (df['wake_time'] - df['sleep_time']).dt.total_seconds() / 3600
df['sleep_duration_hours'] = df['sleep_duration_hours'].apply(lambda x: x+24 if x<0 else x)
df['sleep_duration_hours'] = df['sleep_duration_hours'].fillna(7.0)

# Final selected features
features = ['sleep_duration_hours', 'meals_skipped', 'stress', 'mood', 'traffic', 'screen_time']

# Fill missing values
df = df.fillna({
    'meals_skipped': 'No',
    'stress': 3,
    'mood': 'Neutral',
    'traffic': 'No',
    'screen_time': 1
})

# 🛠 Label Encode categorical columns
label_encoders = {}

for col in ['meals_skipped', 'mood', 'traffic']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Save encoder if you need reverse mapping later

# Function to train and save models
def train_and_save_model(target_column, output_file):
    X = df[features]
    y = df[target_column]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    with open(f'src/{output_file}', 'wb') as f:
        pickle.dump(model, f)

# Train and save models
train_and_save_model('Diet Suggestions', 'diet_model.pkl')
train_and_save_model('Workout Suggestions', 'workout_model.pkl')
train_and_save_model('Sleep Habit Suggestions', 'sleep_habit_model.pkl')
train_and_save_model('Stress Busters', 'stress_busters_model.pkl')

print("✅ All models trained and saved correctly!")
