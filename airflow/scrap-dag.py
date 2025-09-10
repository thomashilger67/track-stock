from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

default_args = {
    'owner': 'thlr',
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}

with DAG(
    dag_id='track-stock-dag',
    default_args=default_args,
    description='Run track stock scrapper every day',
    schedule="@daily",
    start_date=datetime(2025, 9, 9),
    catchup=False
) as dag:

    run_ecs_task = EcsRunTaskOperator(
        task_id="runs_track_stock_scrapper_on_ecs",
        cluster="track-stock",          
        task_definition="track-stock-scrapping",     
        launch_type="FARGATE",
        aws_conn_id="aws_default",
        overrides={
        "containerOverrides": [
            {
                "name": "track-stock",
                "environment": [
                    {
                        "name": "TICKERS",
                        "value": "UUUU GOOGL AMZN ONON NVDA NOV"
                    }
                ]
                
            },
        ],
    },
    network_configuration={
        "awsvpcConfiguration": {
            "subnets": ["subnet-0387a94bd186f8982","subnet-0ea48fb1ca37d2ef0","subnet-04a097f5c85139be6"],
            "assignPublicIp": "ENABLED"
        }
    }
        
    )

    glue_job_task = GlueJobOperator(
        task_id="glue_job_task",
        job_name="Transform from S3",
        script_location=f"s3://aws-glue-assets-156999051389-eu-north-1/scripts/Transform from S3.py",
        aws_conn_id="aws_default",
        region_name="eu-north-1",
        wait_for_completion=True)

    run_ecs_task >> glue_job_task
