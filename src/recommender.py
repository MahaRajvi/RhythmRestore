import pandas as pd
import pickle

# Function to load a model from file
def load_model(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Load all models into a dictionary
model_bundle = {}
try:
    model_bundle["Diet"] = load_model("src/diet_model.pkl")
except Exception as e:
    print(f"Failed to load Diet model: {e}")

try:
    model_bundle["Workout"] = load_model("src/workout_model.pkl")
except Exception as e:
    print(f"Failed to load Workout model: {e}")

try:
    model_bundle["Sleep Habits"] = load_model("src/sleep_habit_model.pkl")
except Exception as e:
    print(f"Failed to load Sleep Habits model: {e}")

try:
    model_bundle["Stress Busters"] = load_model("src/stress_busters_model.pkl")
except Exception as e:
    print(f"Failed to load Stress Busters model: {e}")

print("Loaded Models:", model_bundle.keys())

# 🛠️ Function to convert screen time string to float
def convert_screen_time(val):
    if isinstance(val, str):
        if 'Less' in val:
            return 0.5
        elif '1' in val:
            return 1.0
        elif '2' in val:
            return 2.0
        elif '3' in val:
            return 3.0
        elif 'More' in val:
            return 4.0
        else:
            return 1.0
    return val

# 🛠️ Main function to get recommendations
def get_recommendations(user_input):
    # Create a DataFrame from user input
    df = pd.DataFrame([user_input])

    # Fill default values where missing
    defaults = {
        "meals_skipped": "No",
        "stress": 3,
        "mood": "Neutral",
        "traffic": "No",
        "screen_time": 1
    }

    for col, default_value in defaults.items():
        if col not in df.columns or df[col].isnull().any() or (df[col] == '').any():
            df[col] = df[col].replace('', default_value).fillna(default_value)

    # 🛠️ Calculate sleep duration
    try:
        df['sleep_time'] = pd.to_datetime(df['sleep_time'], format='%H:%M:%S', errors='coerce')
        df['wake_time'] = pd.to_datetime(df['wake_time'], format='%H:%M:%S', errors='coerce')

        df['sleep_duration_hours'] = (df['wake_time'] - df['sleep_time']).dt.total_seconds() / 3600
        df['sleep_duration_hours'] = df['sleep_duration_hours'].apply(lambda x: x + 24 if x < 0 else x)
        df['sleep_duration_hours'] = df['sleep_duration_hours'].fillna(7.0)
    except:
        df['sleep_duration_hours'] = 7.0

    # 🛠️ Encode categorical features
    label_maps = {
        'meals_skipped': {'No': 0, 'Sometimes': 1, 'Often': 2},
        'mood': {'Neutral': 0, 'Happy': 1, 'Sad': 2, 'Anxious': 3},
        'traffic': {'No': 0, 'Yes': 1}
    }

    for col, mapping in label_maps.items():
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(0)

    # 🛠️ Convert screen_time properly
    if 'screen_time' in df.columns:
        df['screen_time'] = df['screen_time'].apply(convert_screen_time)

    # 🛠️ Arrange columns in expected order
    expected_order = ['sleep_duration_hours', 'meals_skipped', 'stress', 'mood', 'traffic', 'screen_time']
    df = df[expected_order]

    print("Input to models:")
    print(df)

    # 🛠️ Generate predictions
    results = {}
    for category, model in model_bundle.items():
        prediction = model.predict(df)[0]
        results[category] = prediction

    return results
if __name__ == '__main__':
    sample_input = {
        "sleep_time": "22:00:00",
        "wake_time": "06:00:00",
        "meals_skipped": "No",
        "stress": 2,
        "mood": "Happy",
        "traffic": "No",
        "screen_time": "1"
    }

    recommendations = get_recommendations(sample_input)
    print("Recommendations based on sample input:")
    print(recommendations)
