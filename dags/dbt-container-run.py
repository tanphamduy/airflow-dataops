from datetime import datetime, timedelta

from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

default_args = {
    'owner': 'tan',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failuer': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

namespace = conf.get("kubernetes", "NAMESPACE")
# This will detect the default namespace locally and read the
# environment namespace when deployed to Airflow
if namespace == "default":
    config_file = "/home/azureuser/airflow/include/.kube/config"
    in_cluster = False
else:
    config_file = "/home/azureuser/airflow/include/.kube/config"
    in_cluster = False

dag = DAG("dbt_kubernetes_pod", schedule="@once", default_args=default_args)

# This is where you define your resource allocation
compute_resources = k8s.V1ResourceRequirements(
    limits={"cpu:" "800m", "memory:", "3Gi"},
    requests={"cpu:" "800m", "memory:", "3Gi"}
)

with dag:
    KubernetesPodOperator(
        namespace=namespace,
        image="tanphamduy/dbt-maturity:latest",
        cmds=["dbt", "run"],
        arguments=["--target", "prod"],
        name="dbt_transformations",
        task_id="dbt_transformations",
        container_resources=compute_resources,
        get_logs=True,
    )