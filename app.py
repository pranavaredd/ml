from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the pretrained model
clf = joblib.load("./model_data/boston_housing_prediction.joblib")

# Initialize Flask app
app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


def scale(payload):
    """Scales Payload"""
    LOG.info(f"Scaling Payload: \n{payload}")
    scaler = StandardScaler().fit(payload.astype(float))
    scaled_adhoc_predict = scaler.transform(payload.astype(float))
    return scaled_adhoc_predict


@app.route("/")
def home():
    return "<h3>Sklearn Prediction Home</h3>"


@app.route("/predict", methods=['POST'])
def predict():
    """Performs an sklearn prediction
        input format:
        {
            "CHAS": {"0":0},
            "RM": {"0":6.575},
            "TAX": {"0":296.0},
            "PTRATIO": {"0":15.3},
            "B": {"0":396.9},
            "LSTAT": {"0":4.98}
        }

        output format:
        { "prediction": [ <val> ] }
    """

    # Logging the input payload
    json_payload = request.json
    LOG.info(f"JSON payload: \n{json_payload}")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info(f"Inference payload DataFrame: \n{inference_payload}")

    # Scale the input data
    scaled_payload = scale(inference_payload)

    # Get the prediction from the pretrained model
    prediction = list(clf.predict(scaled_payload))

    # Log the output prediction value
    LOG.info(f"Output Prediction: {prediction}")

    # Return prediction in JSON format
    return jsonify({'prediction': prediction})


if __name__ == "__main__":
    # Run the Flask application
    app.run(host='0.0.0.0', port=80, debug=True)
