import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Generate dummy cyber incident data
np.random.seed(42)
n_samples = 100

# Features: [num_alerts, attack_duration_sec, num_targets]
X = np.column_stack([
    np.random.poisson(5, n_samples),     # num_alerts
    np.random.exponential(300, n_samples),  # attack_duration_sec
    np.random.randint(1, 10, n_samples)  # num_targets
])

# Target: severity class (0=low,1=medium,2=high)
# Simple rule: high if num_alerts>7 or duration>400 or targets>7, else medium or low randomly
y = []
for a, d, t in X:
    if a > 7 or d > 400 or t > 7:
        y.append(2)  # high severity
    else:
        y.append(np.random.choice([0,1], p=[0.6,0.4]))

y = np.array(y)

# Train a simple Random Forest classifier
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X_train, y_train)

# Predict on all data
y_pred = clf.predict(X)

# Create output JSON structure
severity_map = {0: "Low", 1: "Medium", 2: "High"}

incidents = []
for i, (alerts, duration, targets) in enumerate(X):
    incidents.append({
        "id": i,
        "num_alerts": int(alerts),
        "attack_duration_sec": float(duration),
        "num_targets": int(targets),
        "severity": severity_map[y_pred[i]],
        "severity_score": int(y_pred[i])
    })

# Save to JSON
with open("incidents.json", "w") as f:
    json.dump(incidents, f, indent=2)

print("incidents.json generated with classified incidents.")
