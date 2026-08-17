# ============================================================
# DATABASE TABLE MODEL
# ============================================================

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


# ============================================================
# STUDENT PREDICTION TABLE
# ============================================================

class StudentPrediction(Base):

    # Name of the database table
    __tablename__ = "student_predictions"


    # --------------------------------------------------------
    # Unique ID for each prediction
    # --------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # --------------------------------------------------------
    # Student information
    # --------------------------------------------------------
    gender = Column(
        String,
        nullable=False
    )

    race_ethnicity = Column(
        String,
        nullable=False
    )

    parental_education = Column(
        String,
        nullable=False
    )

    lunch = Column(
        String,
        nullable=False
    )

    test_preparation = Column(
        String,
        nullable=False
    )


    # --------------------------------------------------------
    # Machine learning prediction
    # --------------------------------------------------------

    prediction = Column(
        String,
        nullable=False
    )


    # --------------------------------------------------------
    # Probability of each prediction
    # --------------------------------------------------------

    needs_improvement_probability = Column(
        Float,
        nullable=False
    )

    pass_probability = Column(
        Float,
        nullable=False
    )

    # --------------------------------------------------------
    # Date and time of prediction
    # --------------------------------------------------------
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )