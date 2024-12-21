from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1)
}

with DAG('etl_to_postgres', default_args=default_args, schedule_interval=None) as dag:
    etl_process = BashOperator(
        task_id='etl_process',
        bash_command='python /opt/airflow/scripts/etl_pipeline.py'
    )
