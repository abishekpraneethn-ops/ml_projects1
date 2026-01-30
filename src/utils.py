import os
import pickle
import sys


def save_object(file_path: str, obj):
    """
    Save a Python object to disk using pickle.
    Circular-import safe version.
    """
    try:
        # Import INSIDE function to avoid circular imports
        from src.exception import CustomException
        from src.logger import get_logger

        logger = get_logger(__name__)

        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file:
            pickle.dump(obj, file)

        logger.info(f"Object saved successfully at {file_path}")

    except Exception as e:
        from src.exception import CustomException
        raise CustomException(e, sys)
