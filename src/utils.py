import os
import sys
import pickle

import numpy as np
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging


def save_object(file_path, obj):
    """
    Save a Python object as a pickle file
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info(f"Saved object at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    """
    Load a pickled Python object
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models):
    """
    Train and evaluate multiple ML models
    Returns:
        dict: model_name -> r2 score
    """
    try:
        report = {}

        for model_name, model in models.items():
            logging.info(f"Training model: {model_name}")

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            score = r2_score(y_test, y_pred)
            report[model_name] = score

            logging.info(f"{model_name} R2 score: {score}")

        return report

    except Exception as e:
        raise CustomException(e, sys)
