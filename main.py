from networksecurity.components.data_ingestion import DataIngestion


from networksecurity.Exception.Exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.Entity.config_entity import DataIngestionConfig
from networksecurity.Entity.config_entity import TrainingPipelineConfig

import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

        
        
    except Exception as e:
           raise NetworkSecurityException(e,sys)