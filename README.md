# track-stock
This small project implements a cloud-ready and production-ready ETL pipeline for financial data using AWS and Apache Airflow.

## 🌟 Highlights

- **Orchestration:** Automated with Apache Airflow
- **Cloud-native:** Runs on AWS (ECS, Glue, S3)
- **Extensible:** Easily add new tickers or transformations
- **Modern stack:** Dockerized for portability, Spark for parallelism and scale, use of Apache Iceberg for a modern data lakehouse


## ℹ️ Overview
The pipeline works in two main steps:
1. **Extraction:** An ECS container runs a python script [`extract/main.py`](extract/main.py) to fetch stock data and stores it in a S3 bucket. 

2. **Transformation  & Load :** An AWS Glue job ([`glue/Transform from S3.py`](glue/Transform%20from%20S3.py)) reads the raw data from S3, transformes it and writes it into a Apache Iceberg table.

Data is then accessible and queryable in SQL from Amazon Athena in a form of a data lakehouse

Airflow orchestrates the entire process via [`airflow/track-stock-dag.py`](airflow/track-stock-dag.py).


## 🚀 Quick-start 

### Prerequisties 

- An AWS account with permissions for ECS, Glue, and S3
- A working Airflow infrastructure
- Docker installed (for building the extraction image)

### Setup Steps

1. **Create the required S3 buckets:**
   - One for raw archives
   - One for Glue scripts
   - One for the data warehouse

2. **Upload the Glue script:**
   - Upload [`glue/Transform from S3.py`](glue/Transform%20from%20S3.py) to your Glue scripts S3 bucket.

3. **Configure Airflow:**
   - Update `script_location` in [`airflow/track-stock-dag.py`](airflow/track-stock-dag.py) with your S3 path to the Glue script.
   - Place [`airflow/track-stock-dag.py`](airflow/track-stock-dag.py) in your Airflow `dags` folder.
   - Set up an AWS connection in Airflow named `aws_default` with the necessary permissions.

4. **Build and push the extraction Docker image:**
   - In the `extract/` folder, run:

     ```sh
     ./build.sh
     ```
   - This builds and pushes the image to your ECR registry.

5. **Launch the DAG:**
   - In the Airflow UI, enable and trigger the `track-stock-dag`.


## 📝 Customization

- To add tickers, update the Airflow DAG file as needed.
- To change the schedule, modify the `schedule` parameter in the DAG.
