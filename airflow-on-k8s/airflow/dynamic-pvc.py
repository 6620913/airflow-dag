from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import yaml
import tempfile



def create_pvc(pvc_name,storage_size):

    create_pvc_dic = {
        'apiVersion': 'v1',
        'kind': 'PersistentVolumeClaim',
        'metadata': {
            'name': pvc_name
        },
        'spec': {
            'accessModes': ['ReadWriteOnce'],
            'resources': {
                'requests': {
                    'storage': storage_size
                }
            }
        }
    }


    create_pvc_yaml_string = yaml.dump(create_pvc_dic)


    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(create_pvc_yaml_string)
    return temp_file.name

pvcyaml=create_pvc("my-pvc","1G")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dynamic_pvc',
    default_args=default_args,
    description='DAG for dynamic pvc',
    schedule_interval=None,
)

# Task to create PVC
create_pvc_task = KubernetesPodOperator(
    task_id='create_pvc',
    name='create-pvc',
    namespace='airflow', 
    image='bitnami/kubectl:latest',  
    cmds=['kubectl'],
    arguments=['apply', '-f', pvcyaml],
    service_account_name='airflow-worker',
    dag=dag,
)


def print_something():
    print("This is a message printed by the print_something task.")

print_something_task = PythonOperator(
    task_id='print_something',
    python_callable=print_something,
    dag=dag,
)

# Task to delete PVC
delete_pvc_task = KubernetesPodOperator(
    task_id='delete_pvc',
    name='delete-pvc',
    namespace='airflow', 
    image='bitnami/kubectl:latest', 
    cmds=['kubectl'],
    arguments=['delete', 'pvc', 'my-pvc'],
    service_account_name='airflow-worker',
    dag=dag,
)

# Define the sequence of tasks
create_pvc_task >> print_something_task >> delete_pvc_task
