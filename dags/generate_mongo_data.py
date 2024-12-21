from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1)
}

with DAG('generate_mongo_data', default_args=default_args, schedule_interval=None) as dag:
    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='python /opt/airflow/scripts/data_generator.py'
    )
