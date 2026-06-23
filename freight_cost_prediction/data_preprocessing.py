# 1. Standard Database & Data Manipulation Libraries
import sqlite3
import pandas as pd

# 2. Data Visualization Libraries
import matplotlib.pyplot as plt
import seaborn as sns

# 3. Machine Learning: Data Splitting
from sklearn.model_selection import train_test_split

# 4. Machine Learning: Regression Models
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

# 5. Machine Learning: Evaluation Metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_vendor_invoice_data(db_path: str):
    """
    Load vendor invoice data from SQLite database.
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM vendor_invoice"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def prepare_features(df: pd.DataFrame):
    """
    Select features and target variable.
    """
    X = df[["Dollars"]]
    y = df["Freight"]
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split dataset into train and test sets.
    """
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )