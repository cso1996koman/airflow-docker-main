from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
from datetime import datetime
import pandas as pd
import os


def generate_data(**kwargs):
    # 현재 경로
    current_path = os.getcwd()
    print("Current Directory Path:", current_path)

    file_list = os.listdir(current_path)
    print("Files in Directory:", file_list)

    # 예시 데이터 생성
    data = {'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']}
    df = pd.DataFrame(data)

    # CSV 파일로 저장
    file_path = '/opt/airflow/tmp/example_data.csv'
    df.to_csv(file_path, index=False)

    # 파일 경로를 다음 태스크로 넘기기 위해 XCom에 저장
    kwargs['ti'].xcom_push(key='file_path', value=file_path)


def upload_to_hdfs(**kwargs):
    # XCom에서 파일 경로 가져오기
    ti = kwargs['ti']
    file_path = ti.xcom_pull(key='file_path', task_ids='generate_data')

    # WebHDFS 연결
    hdfs_hook = WebHDFSHook(webhdfs_conn_id='local_hdfs')
    hdfs_client = hdfs_hook.get_conn()

    # HDFS에 파일 업로드
    hdfs_client.upload('/test/data/example_data.csv', file_path)

    # 로컬 파일 삭제
    os.remove(file_path)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 8, 1),
}

with DAG(dag_id='hdfs_save', default_args=default_args, schedule_interval='@once') as dag:
    generate_data_task = PythonOperator(
        task_id='generate_data',
        python_callable=generate_data,
        provide_context=True
    )

    upload_to_hdfs_task = PythonOperator(
        task_id='upload_to_hdfs',
        python_callable=upload_to_hdfs,
        provide_context=True
    )

    generate_data_task >> upload_to_hdfs_task