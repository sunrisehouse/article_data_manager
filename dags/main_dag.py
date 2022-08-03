import os
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.mysql.hooks.mysql import MySqlHook

AWS_CONN_ID = 'aws_default'
SOURCE_BUCKET_NAME = 'jungwoohan-temp-source-bucket'
FILE_NAME = 'temp.csv'
TARGET_BUCKET_NAME = 'jungwoohan-l0-bucket'

def task_s3_log_load():
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    keys = hook.list_keys(SOURCE_BUCKET_NAME)
    for key in keys:
        print(key)
        obj = hook.get_key(key, SOURCE_BUCKET_NAME)
        print(obj.bucket_name, obj.key)

def download_from_s3(key: str, bucket_name: str, local_path: str) -> str:
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    file_name = hook.download_file(key=key, bucket_name=bucket_name, local_path=local_path)
    return file_name

def rename_file(ti, new_name: str) -> None:
    downloaded_file_name = ti.xcom_pull(task_ids=['download_from_s3'])
    downloaded_file_path = '/'.join(downloaded_file_name[0].split('/')[:-1])
    os.rename(src=downloaded_file_name[0], dst=f"{downloaded_file_path}/{new_name}")

def upload_to_s3(filename: str, key: str, bucket_name: str) -> None:
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)

def create_table():
    hook = MySqlHook(mysql_conn_id='mysql_default')
    hook.run("CREATE TABLE test_table")

with DAG(
    dag_id='main',
    schedule_interval='@daily',
    start_date=datetime(2022, 3, 1),
    catchup=False
) as dag:
    mysql_create_operator = PythonOperator(
        task_id='create_table',
        python_callable=create_table,
    )

    # Download a file
    task_download_from_s3 = PythonOperator(
        task_id='download_from_s3',
        python_callable=download_from_s3,
        op_kwargs={
            'key': FILE_NAME,
            'bucket_name': SOURCE_BUCKET_NAME,
            'local_path': './'
        }
    )

    # Rename the file
    task_rename_file = PythonOperator(
        task_id='rename_file',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'temp.csv'
        }
    )

    # Upload the file
    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        op_kwargs={
            'filename': f'./{FILE_NAME}',
            'key': FILE_NAME,
            'bucket_name': TARGET_BUCKET_NAME
        }
    )

    mysql_create_operator >> task_download_from_s3 >> task_rename_file >> task_upload_to_s3
