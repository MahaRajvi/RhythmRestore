import pickle
import pandas as pd

model_files = {
    "Diet Suggestions": "src/diet_model.pkl",
    "Workout Suggestions": "src/workout_model.pkl",
    "Sleep Habit Suggestions": "src/sleep_habit_model.pkl",
    "Stress Busters": "src/stress_busters_model.pkl"
}

label_data = []

for category, path in model_files.items():
    with open(path, "rb") as f:
        model_bundle = pickle.load(f)
        labels = model_bundle["target_encoder"].classes_
        for i, label in enumerate(labels):
            label_data.append({
                "Category": category,
                "Class Index": i,
                "Recommendation": label
            })

df = pd.DataFrame(label_data)
df.to_excel("Model_Recommendations_Lookup.xlsx", index=False)
print("✅ Exported to Model_Recommendations_Lookup.xlsx")
