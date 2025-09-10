from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator


default_args = {
    'owner': 'thlr',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='track-stock-dag',
    default_args=default_args,
    description='Run track stock scrapper every 12 hours',
    schedule=timedelta(hours=12),
    start_date=datetime(2025, 9, 9),
    catchup=False
) as dag:

    run_ecs_task = EcsRunTaskOperator(
        task_id="run_ecs_track_stock",
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

    run_ecs_task
