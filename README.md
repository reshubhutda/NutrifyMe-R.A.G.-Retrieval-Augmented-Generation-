python -m venv .venv

.venv\Scripts\activate

mkdir airflow
cd airflow

curl -LfO https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml

mkdir config dags logs plugins

init