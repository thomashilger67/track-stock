# track-stock
This small project iams to implement a cloud-ready and production-ready ETL pipeline for financial data.

## 🌟 Highlights



## Quick-start 
The pipeline uses Apache Airflow for ochestration and AWS as cloud-provider. To start the ETL, you shall have a working Airflow inrastructure ready and an AWS account with enough credit and the right IAM role to launch ECS and glue Job:

- create all mandaotry S3-bucket : extract, glue, glue Warehouse. 
- deposit glue/`Transform from s3` on AWS in a S3 bucket.
- modify  script_location in airflow/`track-stock-dag.py` with your correct S3 path.
- drop airflow/`track-stock-dag.py` in your airflow/dags folder 
- configure airflow to add an aws account named `aws_default` and the corresponding rights
- ready to launch DAG
