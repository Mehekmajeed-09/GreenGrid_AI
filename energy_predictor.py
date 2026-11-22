import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Sample training data (simulated)
# Features: hour, temperature, previous demand
X = np.array([
    [6, 22, 100],
    [8, 25, 150],
    [10, 28, 180],
    [12, 32, 220],
    [14, 34, 250],
    [16, 30, 230],
    [18, 27, 300],
    [20, 25, 350],
    [22, 23, 200],
    [7, 24, 120],
    [9, 26, 160],
    [13, 33, 240],
    [17, 29, 260],
    [19, 26, 320]
])

# Target: actual simulated household demand (W)
y = np.array([
    110, 160, 190, 230, 260,
    240, 310, 360, 210, 130,
    170, 250, 270, 330
])

# Create and train the model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_demand(hour, temperature, previous_demand):
    """Predict household electricity demand in watts."""

    input_data = np.array([[
        hour,
        temperature,
        previous_demand
    ]])

    prediction = model.predict(input_data)

    return round(float(prediction[0]), 2)