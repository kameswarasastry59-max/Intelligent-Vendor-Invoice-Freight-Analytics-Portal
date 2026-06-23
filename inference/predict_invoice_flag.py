import joblib
import pandas as pd

MODEL_PATH = "models/predict_flag_invoice.pkl"

def load_model(model_path: str = MODEL_PATH):
    """
    Load trained classifier model.
    """
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    return model

def predict_invoice_flag(input_data):
    """
    Predict invoice flag for new vendor invoices.
    
    Parameters
    ----------
    input_data : dict
    
    Returns
    -------
    pd.DataFrame with predicted flag
    """
    model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df['Predicted_Flag'] = model.predict(input_df).round()
    return input_df

if __name__ == "__main__":
    # Example inference run (local testing)
    # Using the 5 specific features the Random Forest was trained on
    sample_data = {
        "invoice_quantity": [50, 10],            # Invoice 1 is normal, Invoice 2 has low quantity
        "invoice_dollars": [500.00, 15000.00],   # Invoice 2 has a huge dollar amount
        "Freight": [25.00, 450.00],              # Invoice 2 has massive freight
        "total_item_quantity": [50, 8],          # Mismatch for Invoice 2 (10 vs 8)
        "total_item_dollars": [500.00, 14000.00] # Mismatch for Invoice 2 ($15k vs $14k)
    }
    
    prediction = predict_invoice_flag(sample_data)
    print(prediction)