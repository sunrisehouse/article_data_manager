import os
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.mysql.hooks.mysql import MySqlHook

from naver_article_crawler import ArticleCrawler, ArticleListFromPressCrawler
from time import sleep

AWS_CONN_ID = 'aws_default'
SOURCE_BUCKET_NAME = 'jungwoohan-temp-source-bucket'
FILE_NAME = 'temp.csv'
TARGET_BUCKET_NAME = 'jungwoohan-l0-bucket'

def hello():
    print('hello hh')

def crawl_a_day(oid, date):
    naver_press_article_list_crawler = ArticleListFromPressCrawler()
    a_list = naver_press_article_list_crawler.crawl(oid, date)
    data = []
    for a in a_list:
        print(a.get('title'))
        naver_article_crawler = ArticleCrawler()
        data.append(naver_article_crawler.crawl(a.get('href')))
        sleep(3)

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
    hello_operator = PythonOperator(
        task_id='hello_operator',
        python_callable=hello,
    )

    crawl_operator = PythonOperator(
        task_id='crawl_a_day',
        python_callable=crawl_a_day,
        op_kwargs={
            'oid': '032',
            'date': '20220803',
            'local_path': './'
        }
    )

    hello_operator >> crawl_operator
