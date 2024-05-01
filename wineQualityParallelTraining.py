"""
    UCID:   sfd6
    Project:   Wine Quality Assessment
"""

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassifier
from pyspark.sql.types import IntegerType, FloatType
from pyspark.ml.feature import VectorAssembler
from io import BytesIO
import os
import boto3
import subprocess
import tarfile

"""
    Initialize Spark Application
"""

APP_NAME = "Wine Quality Analysis App"
spark_conf = SparkConf().setAppName(APP_NAME)
spark_context = SparkContext(conf=spark_conf)

spark_sess = SparkSession.builder.appName(APP_NAME).getOrCreate()

"""
    Fetch and preprocess training dataset from S3.
"""

s3_client = boto3.client('s3')
response = s3_client.get_object(Bucket='sfd6-ml-files', Key='TrainingDataset.csv')
training_data = response['Body'].read().decode('utf-8')
training_data = training_data.replace('"', '')
data_lines = training_data.split('\r\n')
parsed_data = [tuple(line.split(';')) for line in data_lines[1:-1]]
header = data_lines[0].split(';')

df_train = spark_sess.createDataFrame(parsed_data, header)

df_train = df_train.select(*(col(c).cast(FloatType()).alias(c) for c in header[:-1]), col(header[-1]).cast(IntegerType()).alias('label'))

"""
    Configure and train RandomForest model.
"""
features_assembler = VectorAssembler(inputCols=header[:-1], outputCol='features')
df_train = features_assembler.transform(df_train)

rf_classifier = RandomForestClassifier(featuresCol='features', labelCol='label')
model = rf_classifier.fit(df_train)

"""
    Save and export the trained model.
"""
model_path = '/tmp/rf_model'
model.write().overwrite().save(model_path)

# Packaging model into a tarball for S3 upload
tar_path = "WineQualityModel.tar.gz"
with tarfile.open(tar_path, "w:gz") as tar:
    tar.add(model_path, arcname=os.path.basename(model_path))

s3_client.upload_file(Filename=tar_path, Bucket='sfd6-ml-files', Key='WineQualityModel.tar.gz')

"""
    Load and evaluate model on validation data.
"""
validation_response = s3_client.get_object(Bucket='sfd6-ml-files', Key='ValidationDataset.csv')
validation_data = validation_response['Body'].read().decode('utf-8').replace('"', '')
validation_lines = validation_data.split('\r\n')
parsed_validation_data = [tuple(line.split(';')) for line in validation_lines[1:-1]]

df_validation = spark_sess.createDataFrame(parsed_validation_data, header)
df_validation = df_validation.select(*(col(c).cast(FloatType()).alias(c) for c in header[:-1]), col(header[-1]).cast(IntegerType()).alias('label'))
df_validation = features_assembler.transform(df_validation)

predictions = model.transform(df_validation)

# Cleanup local and HDFS environments
subprocess.run("rm -rf /tmp/rf_model", shell=True)
subprocess.run("rm " + tar_path, shell=True)
spark_context.stop()
