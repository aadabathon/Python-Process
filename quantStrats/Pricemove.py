import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf

np.random.seed(42)

# ---- Generate synthetic price series ----
N = 2000
price = np.cumsum(np.random.normal(0, 1, N)) + 100

# ---- Build features: returns over last 5 steps ----
window = 5
X = np.array([price[i:i+window] for i in range(N-window-1)])
y = (np.diff(price)[window:] > 0).astype(int)   # 1 = up, 0 = down

# ---- Scale ----
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---- Train/Test Split ----
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, shuffle=False
)

# ---- Build TensorFlow Model ----
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# ---- Train ----
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=32,
    verbose=0
)

# ---- Evaluate ----
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy:", round(acc, 4))

# ---- Plot training curve ----
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='val')
plt.legend()
plt.title("Training Loss")
plt.show()

# ---- Predict next movement ----
next_input = price[-window:]
next_input_scaled = scaler.transform([next_input])
prob_up = model.predict(next_input_scaled)[0][0]

print("Next movement probability (up):", round(prob_up, 3))
