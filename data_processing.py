import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def load_data():
    # Load the data
    data = pd.read_csv('job_offers_net_empregos.csv')
    return data

def preprocess_data(data):
    # check for missing values
    missing_values = data.isnull().sum()
    
    return data

def split_data(data):
    # Split the data into features and target
    X = data.drop('diagnosis', axis=1)
    y = data['diagnosis']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

def scale_data(X_train, X_test):
    # Scale the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test

def main():
    # Load the data
    data = load_data()
    
    # Preprocess the data
    data = preprocess_data(data)
    
    # # Split the data
    # X_train, X_test, y_train, y_test = split_data(data)
    
    # # Scale the data
    # X_train, X_test = scale_data(X_train, X_test)
    
    print('Data processing complete.')
