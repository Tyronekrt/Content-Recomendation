import os
import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import pickle
from surprise import accuracy


# Step 1: Load the data
file_path = 'celery.py'
columns = ['user_id', 'item_id', 'rating', 'timestamp']
try:
    print("Loading data...")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at: {file_path}")
    data = pd.read_csv(file_path, sep='::', names=columns, engine='python')
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")
    raise

# Step 2: Prepare the data for the Surprise library
try:
    print("Preparing dataset for the Surprise library...")
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(data[['user_id', 'item_id', 'rating']], reader)
    print("Dataset prepared successfully!")
except Exception as e:
    print(f"Error preparing dataset: {e}")
    raise

# Step 3: Split the data into training and testing sets
try:
    print("Splitting data into training and testing sets...")
    training_data, testing_data = train_test_split(dataset, test_size=0.2)
    print("Data split successfully!")
except Exception as e:
    print(f"Error splitting data: {e}")
    raise

# Step 4: Train a collaborative filtering model
try:
    print("Training the collaborative filtering model...")
    model = SVD()
    model.fit(training_data)
    print("Model training completed successfully!")
except Exception as e:
    print(f"Error training the model: {e}")
    raise

# Step 5: Evaluate the model
try:
    print("Evaluating the model...")
    predictions = model.test(training_data)
    rmse = accuracy.rmse(predictions)
    print(f"Model evaluation completed. RMSE: ")
except Exception as e:
    print(f"Error evaluating the model: {e}")
    raise

# Step 6: Save the trained model
model_file_path = 'collaborative_model.pkl'
try:
    print(f"Saving the model to {model_file_path}...")
    with open(model_file_path, 'wb') as model_file:
        pickle.dump(model, model_file)
    if os.path.exists(model_file_path):
        print(f"Model saved successfully at {model_file_path}!")
    else:
        raise FileNotFoundError(f"Model file not created: {model_file_path}")
except Exception as e:
    print(f"Error saving the model: {e}")
    raise
