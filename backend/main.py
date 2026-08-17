# ============================================================
# Student Performance Prediction API
# ============================================================

# FastAPI is used to create the backend API.
from fastapi import FastAPI, Depends

# BaseModel is used to define and validate
# the input received from the website.
from pydantic import BaseModel

# SQLAlchemy Session is used to communicate
# with the database.
from sqlalchemy.orm import Session

# Path is used to create reliable file paths.
from pathlib import Path

# pandas is used to create a DataFrame
# from the received student information.
import pandas as pd

# joblib is used to load the trained
# machine learning model and encoder.
import joblib


from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# DATABASE IMPORTS
# ============================================================

from database import SessionLocal, engine, Base
from models import StudentPrediction


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

# Create the student_predictions table if
# it does not already exist.

Base.metadata.create_all(
    bind=engine
)

# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Student Performance Prediction API",
    description="API for predicting student mathematics performance",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# LOAD TRAINED MODEL AND ENCODER
# ============================================================

# Get the project root directory.
#
# __file__ = backend/main.py
# .parent = backend/
# .parent.parent = project root/

BASE_DIR = Path(__file__).resolve().parent.parent


# Path to the trained model.
MODEL_PATH = (
    BASE_DIR
    / "models"
    / "student_performance_model.pkl"
)


# Path to the trained encoder.
ENCODER_PATH = (
    BASE_DIR
    / "models"
    / "student_performance_encoder.pkl"
)


# Load the trained Random Forest model.
model = joblib.load(MODEL_PATH)


# Load the One-Hot Encoder used during training.
encoder = joblib.load(ENCODER_PATH)


print("Machine learning model loaded successfully.")
print("Encoder loaded successfully.")


# ============================================================
# DATABASE SESSION
# ============================================================

def get_db():

    # Create a database session.
    db = SessionLocal()

    try:

        # Give the database session to the API endpoint.
        yield db

    finally:

        # Close the database connection after
        # the request has finished.
        db.close()


# ============================================================
# DEFINE INPUT DATA STRUCTURE
# ============================================================

class StudentInput(BaseModel):

    # Student's gender
    gender: str

    # Student's race/ethnicity group
    race_ethnicity: str

    # Parent's level of education
    parental_education: str

    # Type of lunch
    lunch: str

    # Test preparation course status
    test_preparation: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Student Performance Prediction API is running"
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(
    student: StudentInput,
    db: Session = Depends(get_db)
):

    # ========================================================
    # 1. CONVERT API INPUT INTO DATASET FORMAT
    # ========================================================

    # The API uses simple names such as
    # race_ethnicity.
    #
    # Our trained encoder expects the ORIGINAL
    # dataset column names.
    
    student_data = {

        "gender": [
            student.gender
        ],

        "race/ethnicity": [
            student.race_ethnicity
        ],

        "parental level of education": [
            student.parental_education
        ],

        "lunch": [
            student.lunch
        ],

        "test preparation course": [
            student.test_preparation
        ]
    }


    # ========================================================
    # 2. CREATE PANDAS DATAFRAME
    # ========================================================

    student_df = pd.DataFrame(
        student_data
    )


    # ========================================================
    # 3. ENCODE THE CATEGORICAL DATA
    # ========================================================

    # Use the SAME encoder that was used
    # during model training.

    student_encoded = encoder.transform(
        student_df
    )


    # ========================================================
    # 4. MAKE THE PREDICTION
    # ========================================================

    prediction = model.predict(
        student_encoded
    )[0]


    # ========================================================
    # 5. GET PREDICTION PROBABILITIES
    # ========================================================

    probabilities = model.predict_proba(
        student_encoded
    )[0]


    # Get the class names from the trained model.

    class_names = model.classes_


    # Create a dictionary containing the probability
    # for each class.

    probability_dict = {

        class_name: float(probability)

        for class_name, probability
        in zip(
            class_names,
            probabilities
        )
    }


    # ========================================================
    # 6. SAVE PREDICTION TO DATABASE
    # ========================================================

    # Create a new database record.

    new_prediction = StudentPrediction(

        gender=student.gender,

        race_ethnicity=student.race_ethnicity,

        parental_education=student.parental_education,

        lunch=student.lunch,

        test_preparation=student.test_preparation,

        prediction=prediction,

        needs_improvement_probability=(
            probability_dict["Needs Improvement"]
        ),

        pass_probability=(
            probability_dict["Pass"]
        )
    )


    # Add the record to the database.

    db.add(
        new_prediction
    )


    # Save the record.

    db.commit()


    # Refresh the object so that the automatically
    # generated ID becomes available.

    db.refresh(
        new_prediction
    )


    # ========================================================
    # 7. RETURN RESULT TO CLIENT
    # ========================================================

    return {

        "id": new_prediction.id,

        "prediction": prediction,

        "probabilities": probability_dict
    }


# ============================================================
# GET ALL SAVED PREDICTIONS
# ============================================================

@app.get("/predictions")
def get_predictions(
    db: Session = Depends(get_db)
):

    # Get all prediction records from the database.
    predictions = db.query(
        StudentPrediction
    ).all()

    # Create a list to store the results.
    results = []

    # Go through each database record.
    for prediction in predictions:

        results.append({

            "id": prediction.id,

            "gender": prediction.gender,

            "race_ethnicity": prediction.race_ethnicity,

            "parental_education": (
                prediction.parental_education
            ),

            "lunch": prediction.lunch,

            "test_preparation": (
                prediction.test_preparation
            ),

            "prediction": prediction.prediction,

            "probabilities": {

                "Needs Improvement":
                    prediction.needs_improvement_probability,

                "Pass":
                    prediction.pass_probability
            },

            "created_at": prediction.created_at
        })

    return results