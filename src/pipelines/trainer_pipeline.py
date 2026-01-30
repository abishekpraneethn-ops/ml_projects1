import sys

from src.components.data_ingestion import dataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import get_logger


def main():
    try:
        logger = get_logger(__name__)
        logger.info("Training pipeline started")

        # ---------------- Data Ingestion ----------------
        data_ingestion = dataIngestion()
        train_path, test_path = data_ingestion.initiate_data_ingestion()

        # ---------------- Data Transformation ----------------
        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
            train_path, test_path
        )

        # ---------------- Model Training ----------------
        model_trainer = ModelTrainer()
        model_name, model_score = model_trainer.initiate_model_trainer(
            train_arr, test_arr
        )

        logger.info(
            f"Training completed | Best model: {model_name} | Score: {model_score}"
        )

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
