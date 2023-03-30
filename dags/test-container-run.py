from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

namespace = conf.get("kubernetes", "NAMESPACE")
# This will detect the default namespace locally and read the
# environment namespace when deployed to Airflow
if namespace == "default":
    config_file = "/home/azureuser/airflow/include/.kube/config"
    in_cluster = False
else:
    config_file = "/home/azureuser/airflow/include/.kube/config"
    in_cluster = False

# This is where you define your resource allocation
compute_resources = k8s.V1ResourceRequirements(
    limits={"cpu:" "800m", "memory:", "3Gi"},
    requests={"cpu:" "800m", "memory:", "3Gi"}
)    

k = KubernetesPodOperator(
        namespace=namespace,
        name="hello-dry-run",
        image="tanphamduy/dbt-maturity:latest",
        cmds=["dbt", "run"],
        arguments=["--target", "prod"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
        container_resources=compute_resources,
    )

k.dry_run()