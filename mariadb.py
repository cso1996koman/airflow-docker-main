from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'mariadb_example',
    default_args=default_args,
    description='A simple DAG to write data to MariaDB',
    schedule_interval='@daily',
)

mariadb_test = MySqlOperator(
    task_id='mariadb_test',
    mysql_conn_id='load_admin_db_mariadb',
    sql="SELECT src_nm, tb_nm, tb_code, version, uri, created_at, dir_path, Column1 FROM api_admin_tb",
    dag=dag,
)

mariadb_test