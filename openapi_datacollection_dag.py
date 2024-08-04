from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5), 
}

class OpenapiDataCollectionDag:
    def __init__(self, api_admin_dao, url_object_factory):
        self.default_args = default_args
        self.api_admin_dao = api_admin_dao
        self.url_object_factory = url_object_factory
    @task()
    def acquireOpenApiUrlInfobyDbOnce() -> list:
        
     
    
    @dag(default_args=default_args, schedule_interval='@daily', description='A simple DAG to write data to MariaDB')
    def get_openapi_datacollection_dag():
        

        mariadb_test()
        