"""
Project Generator Module

Handles the creation of project structure and files
based on selected templates.

Author: Minhaz Alam
Created: 2026-03
"""

import os
from stackify.core.template_engine import render_template


def create_project_structure(project_name: str, mode: str = "full") -> None:
    """
    Create project structure and generate components.

    Args:
        project_name (str): Name of the project
        mode (str): batch | streaming | full
    """
    base_path = os.path.abspath(project_name)

    os.makedirs(base_path, exist_ok=True)

    # Base folders (always created)
    folders = [
        "spark/jobs",
        "config",
    ]
    if mode in ["batch", "full"]:
        folders.append("airflow/dags")
    # Add kafka only if needed
    if mode in ["streaming", "full"]:
        folders.append("kafka")

    # Create folders
    for folder in folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    # Base setup
    create_base_files(base_path, project_name)
    create_docker_compose(base_path, project_name)

    # Batch
    if mode in ["batch", "full"]:
        create_spark_job(base_path)
        create_airflow_dag(base_path, project_name)

    # Streaming
    if mode in ["streaming", "full"]:
        create_kafka_producer(base_path)
        create_spark_streaming_job(base_path)


def create_base_files(base_path: str, project_name: str) -> None:
    """
    Create README, config, and requirements files.
    """

    # README.md (IMPORTANT: no triple backticks issue)
    render_template(
        "base/README.md.j2",
        os.path.join(base_path, "README.md"),
        {"project_name": project_name},
    )

    # config.yaml
    config_path = os.path.join(base_path, "config", "config.yaml")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    config_content = (
        "spark:\n"
        "  master: local[*]\n"
        f"  app_name: \"{project_name}\"\n"
    )

    with open(config_path, "w") as f:
        f.write(config_content)

    # requirements.txt
    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write("pyspark\n")


def create_docker_compose(base_path: str, project_name: str) -> None:
    """
    Create docker-compose.yml file.
    """

    docker_content = f"""
version: '3.8'

services:

  zookeeper:
    image: bitnami/zookeeper:latest
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes
    ports:
      - "2181:2181"

  kafka:
    image: bitnami/kafka:latest
    depends_on:
      - zookeeper
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
    ports:
      - "9092:9092"

  spark:
    image: bitnami/spark:latest
    container_name: {project_name}_spark
    environment:
      - SPARK_MODE=master
    ports:
      - "8080:8080"
      - "7077:7077"
    volumes:
      - ./spark/jobs:/jobs

  airflow:
    image: apache/airflow:2.7.1
    container_name: {project_name}_airflow
    environment:
      - AIRFLOW__CORE__EXECUTOR=SequentialExecutor
    ports:
      - "8081:8080"
    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./spark/jobs:/opt/airflow/spark/jobs
    command: >
      bash -c "airflow db init &&
               airflow webserver & airflow scheduler"
"""

    with open(os.path.join(base_path, "docker-compose.yml"), "w") as f:
        f.write(docker_content)


def create_spark_job(base_path: str) -> None:

    """
    Create a sample PySpark job.
    """

    spark_job = (
        "from pyspark.sql import SparkSession\n\n"
        "spark = SparkSession.builder.appName('StackifyJob').getOrCreate()\n\n"
        "data = [('Alice', 25), ('Bob', 30)]\n"
        "df = spark.createDataFrame(data, ['name', 'age'])\n\n"
        "df.show()\n\n"
        "spark.stop()\n"
    )

    job_path = os.path.join(base_path, "spark", "jobs", "batch_job.py")

    with open(job_path, "w") as f:
        f.write(spark_job)

def create_airflow_dag(base_path: str, project_name: str) -> None:
    """
    Create a simple Airflow DAG to run Spark job.

    Args:
        base_path (str): Absolute path of the project
        project_name (str): Project name
    """

    dag_content = f"""from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {{
    "owner": "stackify",
    "start_date": datetime(2024, 1, 1),
}}

with DAG(
    dag_id="{project_name}_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    run_spark_job = BashOperator(
        task_id="run_spark_job",
        bash_command="python /opt/airflow/spark/jobs/batch_job.py",
    )
"""

    dag_path = os.path.join(base_path, "airflow", "dags", "pipeline_dag.py")

    with open(dag_path, "w") as f:
        f.write(dag_content)

def create_kafka_producer(base_path: str) -> None:
    """
    Create a simple Kafka producer.
    """

    kafka_path = os.path.join(base_path, "kafka")
    os.makedirs(kafka_path, exist_ok=True)

    producer_code = (
        "from kafka import KafkaProducer\n"
        "import json\n"
        "import time\n\n"
        "producer = KafkaProducer(\n"
        "    bootstrap_servers='kafka:9092',\n"
        "    value_serializer=lambda v: json.dumps(v).encode('utf-8')\n"
        ")\n\n"
        "for i in range(100):\n"
        "    data = {'id': i, 'value': i * 10}\n"
        "    producer.send('test-topic', data)\n"
        "    print(f'Sent: {data}')\n"
        "    time.sleep(1)\n"
    )

    with open(os.path.join(kafka_path, "producer.py"), "w") as f:
        f.write(producer_code)

def create_spark_streaming_job(base_path: str) -> None:
    """
    Create Spark Structured Streaming job consuming Kafka.
    """

    job_path = os.path.join(base_path, "spark", "jobs", "streaming_job.py")

    code = (
        "from pyspark.sql import SparkSession\n\n"
        "spark = SparkSession.builder \\\n"
        "    .appName('KafkaStreaming') \\\n"
        "    .getOrCreate()\n\n"
        "df = spark \\\n"
        "    .readStream \\\n"
        "    .format('kafka') \\\n"
        "    .option('kafka.bootstrap.servers', 'kafka:9092') \\\n"
        "    .option('subscribe', 'test-topic') \\\n"
        "    .load()\n\n"
        "value_df = df.selectExpr('CAST(value AS STRING)')\n\n"
        "query = value_df.writeStream \\\n"
        "    .outputMode('append') \\\n"
        "    .format('console') \\\n"
        "    .start()\n\n"
        "query.awaitTermination()\n"
    )

    with open(job_path, "w") as f:
        f.write(code)