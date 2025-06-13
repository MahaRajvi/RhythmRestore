# 🌙 RhythmRestore

**RhythmRestore** is an AI-powered lifestyle recommendation system designed to help users restore and maintain a healthy circadian rhythm. It provides personalized suggestions for sleep, diet, stress, and exercise based on user inputs and scientifically backed rules.

---

## 🔍 Features

- 🌗 Tracks sleep-wake cycles
- 🍽️ Recommends personalized diet plans
- 🧘‍♀️ Suggests stress-busting techniques
- 🏋️ Offers custom workout routines
- 📊 Visualizes user progress
- 🔒 User login and admin dashboard support

---

## 📁 Project Structure

src/
├── main.py # Entry point for the backend logic
├── recommender.py # AI recommendation engine
├── scheduler.py # Time-based automation
├── setup_database.py # Initializes SQLite DB
├── *.pkl # Trained ML models
static/
├── img/ # Icons and illustrations
├── css/ # Custom stylesheets
templates/
├── *.html # Frontend pages (Jinja2/Flask compatible)

yaml
Copy
Edit

---

## 🧠 How It Works

Users input their:
- Sleep time
- Meals skipped
- Mood
- Work stress
- Screen time

The backend processes this and generates tailored suggestions using:
- Rule-based logic
- Trained ML models
- Doctor-backed recommendations

---

## 🚀 Run the Project Locally

```bash
git clone https://github.com/MahaRajvi/RhythmRestore.git
cd RhythmRestore
pip install -r requirements.txt
python src/main.py
🔐 Note
send_sms.py and .env files are excluded from this repo to protect API credentials. Be sure to configure your environment variables locally.

📸 Screenshots



👩‍💻 Built With
Python

Flask

SQLite

HTML/CSS/JS

scikit-learn

Matplotlib

Twilio (SMS – local only)

🙋‍♀️ About the Author
Developed by Megha Rajvi (MahaRajvi)
Final year B.Tech Student passionate about AI, wellness, and full-stack development.

📬 Contact
📧 Email: mahareddymeghareddy@example.com

🌐 GitHub: @MahaRajvi

📄 License
This project is licensed under the MIT License.

yaml
Copy
Edit

---

#### ✅ 4. **Save and close the file**

---

#### 🚀 5. **Push the README to GitHub**

Back in your terminal:

```bash
git add README.md
git commit -m "Added detailed README for RhythmRestore"
git push
