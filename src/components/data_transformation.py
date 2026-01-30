import sys
import os

import pandas as pd
import numpy as np

from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder

from src.exception import CustomException
from src.logger import get_logger
import logging
logger = get_logger(__name__)
from src.utils import save_object

@dataclass
class dataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.datatransformation_config = dataTransformationConfig()

    def get_data_transformer_obj(self):
        try:
            numerical_cols = ["reading_score","writing_score"]
            categorical_cols = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]

            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder())
                ]
            )
            # logging.info("numerical coloumns standard scaling completed!")
            # logging.info("categorical coloumns encoding and standard scaling completed!")

            preprocessing = ColumnTransformer(
                [("num_transformer",num_pipeline,numerical_cols),
                 ("cat_transformer",cat_pipeline,categorical_cols)]
            )

            return preprocessing
        
        except Exception as e:
            raise CustomException(e,sys)
    

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("reading train and test data completed!")
            logging.info("obtaining pre-processing object")
        
            preprocessing_obj = self.get_data_transformer_obj()

            target_col = "math_score"
            numerical_col = ["reading_score","writing_score"]

            input_feature_train_df = train_df.drop(columns=[target_col],axis=1)
            target_feature_train_df = train_df[target_col]

            input_feature_test_df = test_df.drop(columns=[target_col],axis=1)
            target_feature_test_df = test_df[target_col]

            logging.info("Applying preprocessing object on training and testing data frame")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]


            logging.info("Saved pre-processing object")

            save_object(
                file_path = self.datatransformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,test_arr,self.datatransformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
           