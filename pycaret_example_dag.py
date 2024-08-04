from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from pycaret.classification import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'pycaret_example',
    default_args=default_args,
    description='A simple PyCaret DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
)

def load_data():
    # 예제 데이터 로드 (Iris dataset 사용)
    from sklearn.datasets import load_iris
    data = load_iris(as_frame=True)
    df = data.frame
    df['target'] = df['target'].astype('category')
    df.to_csv('/tmp/iris.csv', index=False)

def train_model():
    df = pd.read_csv('/tmp/iris.csv')
    clf = setup(data=df, target='target', silent=True, verbose=False)
    best_model = compare_models()
    save_model(best_model, '/tmp/best_model')

def evaluate_model():
    df = pd.read_csv('/tmp/iris.csv')
    clf = load_model('/tmp/best_model')
    predictions = predict_model(clf, data=df)
    predictions.to_csv('/tmp/predictions.csv', index=False)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

evaluate_model_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag,
)

load_data_task >> train_model_task >> evaluate_model_task