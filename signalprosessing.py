from kivy.app import App
import numpy as np
from scipy.fft import fft

def extract_features(signal):
    freq_data = fft(signal)
    magnitude = np.abs(freq_data)
    return magnitude[:len(magnitude)//2] 
def preprocess_signal(raw_signal):
    # פילטרים, נרמול, סילוק רעש וכו'
    return [x - min(raw_signal) for x in raw_signal]
def analyze_headache(signal):
    avg = sum(signal) / len(signal)
    if avg > 0.5:
        return "יתכן שיש כאב ראש בינוני-חזק"
    return "אין סימן ברור לכאב ראש"
def show_feedback(message):
    print("פידבק למשתמש:", message)

    # 2. פונקציית ניתוח: משווה בין מדידה חדשה לנורמה
def analyze_brain_activity(signal):
    global baseline_data
    if baseline_data is None:
        return "לא הוגדרה נורמה אישית"

    current_mean = sum(signal) / len(signal)
    diff = abs(current_mean - baseline_data["mean"])

    if diff < 0.1:
        return "מוח רגוע"
    elif diff < 0.25:
        return "התבנית חשודה"
    else:
        return "מיגרנה צפויה"
    

    # חלון שמחזיק רק את 500 הדגימות האחרונות
WINDOW_SIZE = 500
signal_window = []

def update_signal_window(new_value):
    signal_window.append(new_value)
    if len(signal_window) > WINDOW_SIZE:
        signal_window.pop(0)  # מוחק את הערך הכי ישן

    return signal_window



import time

signal_window = []

def update_signal_with_time(new_value):
    now = time.time()
    signal_window.append((now, new_value))

    # מסנן רק את הערכים מה־10 שניות האחרונות
    signal_window[:] = [(t, v) for t, v in signal_window if now - t <= 10]

    return [v for _, v in signal_window]
