import sys
import pandas as pd
import boto3
from datetime import datetime
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *

## @params: [JOB_NAME, S3_bucket, manifest_path]
args = getResolvedOptions(sys.argv, ['JOB_NAME','S3_bucket','manifest_path'] )

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

s3 = boto3.client('s3')

spark.conf.set("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog")
spark.conf.set("spark.sql.catalog.glue_catalog.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog")
spark.conf.set("spark.sql.catalog.glue_catalog.warehouse", "s3://track-stock-iceberg/")

manifest_path=args['manifest_path']
bucket=args['S3_bucket']


try :
    df_manifest= pd.read_csv(manifest_path)
    processed_files = set(df_manifest['file_path'].tolist())
except Exception as e:
    print(f"No manifest file detected {e}")
    processed_files = set()


list_all_files = ['s3://'+bucket+'/'+ x['Key'] for x in s3.list_objects_v2(Bucket=bucket)['Contents']]
unprocessed_files = set(list_all_files) - processed_files


if not unprocessed_files:
    print("No new files to process")
    sys.exit(0)

df = spark.read.json(list(unprocessed_files), multiLine=False)\
.withColumn("file_path", input_file_name())


df_transformed = df.withColumn("ticker",regexp_extract("file_path", r"track-stock/([^/]+)/", 1))\
                   .withColumn("Datetime", to_timestamp(col("Datetime"), "yyyy-MM-dd'T'HH:mm:ss.SSSX"))\
                   .withColumn("year", year(col("Datetime"))) \
                   .withColumn("month", month(col("Datetime"))) \
                   .withColumn("day", dayofmonth(col("Datetime")))
  
table_name="stock_data"                 
full_table_name = "glue_catalog.default.stock_data"  

if table_name not in [t.name for t in spark.catalog.listTables("default")]:
    df_transformed.writeTo(full_table_name) \
                  .partitionedBy("year", "month", "day", "Ticker") \
                  .create()

else:
    df_transformed.writeTo(full_table_name) \
                  .partitionedBy("year", "month", "day","ticker") \
                  .append()


new_manifest = pd.DataFrame({
    "file_path": list(unprocessed_files),
    "processed_at": [datetime.utcnow().isoformat()] * len(list(unprocessed_files))
})

if processed_files:

    manifest_df = pd.concat([df_manifest, new_manifest], ignore_index=True)

else: 
    manifest_df = new_manifest

manifest_df.to_csv(manifest_path, mode='a', header=False, index=False)
job.commit()
