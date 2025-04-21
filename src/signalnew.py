import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# ---------- שלב 1: סימולציית נתונים ----------

# נאמר שאלו הנתונים הנורמטיביים שנאספו מראש ממשתמש
baseline_data = np.random.normal(loc=0, scale=1, size=1000)

# ואלו הנתונים החדשים שנקלטו מהאלקטרודה (לדוגמה – עם "חריגה" באמצע)
new_data = np.concatenate([
    np.random.normal(loc=0, scale=1, size=400),
    np.random.normal(loc=5, scale=1, size=200),  # חריגה!
    np.random.normal(loc=0, scale=1, size=400)
])

# ---------- שלב 2: סינון האות ----------
# Bandpass filter – ניקוי רעשים, שמירה על תדרים של EEG (נאמר 1-50Hz)

def bandpass_filter(data, lowcut=1.0, highcut=50.0, fs=250.0, order=4):
    nyq = 0.5 * fs  # תדר נייקוויסט
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

filtered_data = bandpass_filter(new_data)

# ---------- שלב 3: השוואה לפעילות רגילה ----------

baseline_mean = np.mean(baseline_data)
baseline_std = np.std(baseline_data)

# זיהוי חריגה אם ערך עולה על 3 סטיות תקן (או ערך מותאם)
def detect_anomalies(data, threshold=3):
    anomalies = []
    for i, value in enumerate(data):
        z_score = (value - baseline_mean) / baseline_std
        if abs(z_score) > threshold:
            anomalies.append((i, value))
    return anomalies

anomalies = detect_anomalies(filtered_data)

# ---------- שלב 4: התראה ----------
if anomalies:
    print(f"התגלו {len(anomalies)} חריגות – ייתכן תחילתה של מיגרנה!")
else:
    print("אין סימנים למיגרנה כרגע.")

# ---------- (רשות) ציור גרף ----------
plt.figure(figsize=(12, 4))
plt.plot(filtered_data, label="אות מסונן")
if anomalies:
    x_vals, y_vals = zip(*anomalies)
    plt.scatter(x_vals, y_vals, color='red', label="חריגות")
plt.title("איתור מיגרנה מבוסס עיבוד EEG")
plt.xlabel("נקודות בזמן")
plt.ylabel("עוצמה")
plt.legend()
plt.show()
