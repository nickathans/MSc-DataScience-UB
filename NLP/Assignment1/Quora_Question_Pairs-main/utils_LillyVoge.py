import os
import joblib

def save_model_with_overwrite(model, filepath):
    if os.path.isfile(filepath):
        overwrite = input("The file already exists. Do you want to overwrite it? (y/n) ")
        if overwrite.lower() != "y":
            print("Aborting. Model not saved.")
            return
        
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")