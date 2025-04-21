import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# קריאת הנתונים מהקובץ .npy
eeg_data = np.load("synthetic_eeg_data.npy")

# יצירת תוויות אקראיות (לצורך הדגמה)
n_samples = eeg_data.shape[0]
y = np.random.randint(0, 2, n_samples)  # תוויות אקראיות (0 או 1)

# פיצול הנתונים לסט אימון וסט מבחן
X_train, X_test, y_train, y_test = train_test_split(eeg_data, y, test_size=0.2, random_state=42)

# יצירת המודל עם שכבות CNN
model = Sequential()

# שכבת קונבולוציה עם 32 פילטרים, גודל פילטר 3, אקטיבציה ReLU
model.add(Conv1D(32, 3, activation='relu', input_shape=(eeg_data.shape[1], eeg_data.shape[2])))
model.add(MaxPooling1D(pool_size=2))

# שכבת קונבולוציה נוספת
model.add(Conv1D(64, 3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))

# שכבת Flatten
model.add(Flatten())

# שכבת Dense (שכבה מלאה) עם 64 נוירונים
model.add(Dense(64, activation='relu'))

# שכבת Dropout למניעת אוברפיטינג
model.add(Dropout(0.5))

# שכבת פלט (אחת או יותר לפי הצורך)
model.add(Dense(1, activation='sigmoid'))  # אם מדובר בבעיה בינארית (0/1)

# קומפילציה של המודל
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# אימון המודל
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test))

# הערכה על נתוני המבחן
y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5).astype(int)  # המרה לאות 0/1

# מדידת דיוק
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# הצגת גרף דיוק ואובדן
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
