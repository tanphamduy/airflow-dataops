from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

dag = DAG(
    'dbt_maturity_docker_run',
    default_args={
        'owner': 'tan',
        'depends_on_past': False,
        'email': ['tan.phamduy@vib.com.vn'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule="@once",
    start_date=days_ago(2),
)

t1 = BashOperator(task_id='print_date', bash_command='date', dag=dag)

t2 = DockerOperator(
    api_version='1.30',
    docker_url='unix://var/run/docker.sock',  # Set your docker URL
    image='tanphamduy/dbt-maturity:latest',
    command='dbt run --target prod',
    network_mode='bridge',
    task_id='dbt_run',
    dag=dag,
)

t3 = DockerOperator(
    api_version='1.30',
    docker_url='unix://var/run/docker.sock',  # Set your docker URL
    image='tanphamduy/dbt-maturity:latest',
    command='dbt test --target prod',
    network_mode='bridge',
    task_id='dbt_test',
    dag=dag,
)

t4 = BashOperator(task_id='print_finish', bash_command='echo "Task is finished"', dag=dag)


t1 >> t2
t2 >> t3
t3 >> t4