
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import logging
import sys

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load the serialized model pipeline
model = joblib.load("forecast_superkart_sales_model.joblib")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API is running",
        "endpoint": "/v1/predict"
    })


@app.route("/v1/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Extract the model input features
        sample = {
            "Product_Weight": data["Product_Weight"],
            "Product_Sugar_Content": data["Product_Sugar_Content"],
            "Product_Allocated_Area": data["Product_Allocated_Area"],
            "Product_MRP": data["Product_MRP"],
            "Store_Size": data["Store_Size"],
            "Store_Location_City_Type": data["Store_Location_City_Type"],
            "Store_Type": data["Store_Type"],
            "Store_Age_Years": data["Store_Age_Years"],
            "Product_Type_Category": data["Product_Type_Category"],
            "Product_Id_char": data["Product_Id_char"]
        }

        # Convert input into a DataFrame
        input_df = pd.DataFrame([sample])

        # Make prediction
        prediction = model.predict(input_df)[0]

        logger.info(f"Predicted sales: {prediction}")

        return jsonify({
            "predicted_sales": round(float(prediction), 2)
        })

    except KeyError as e:
        return jsonify({
            "error": f"Missing input field: {str(e)}"
        }), 400

    except Exception as e:
        logger.exception("Prediction failed")
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500

@app.route("/v1/predictbatch", methods=["POST"])
def predict_batch():
    try:
        if "file" not in request.files:
            return jsonify({
                "error": "No file provided"
            }), 400

        file = request.files["file"]

        # Read uploaded CSV into a DataFrame
        batch_data = pd.read_csv(file)

        # Generate predictions for all rows
        predictions = model.predict(batch_data)

        # Return predictions as JSON
        results = {
            str(index): round(float(prediction), 2)
            for index, prediction in enumerate(predictions)
        }

        logger.info(
            f"Batch prediction completed for {len(predictions)} records"
        )

        return jsonify(results)

    except Exception as e:
        logger.exception("Batch prediction failed")
        return jsonify({
            "error": f"Batch prediction failed: {str(e)}"
        }), 500
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
