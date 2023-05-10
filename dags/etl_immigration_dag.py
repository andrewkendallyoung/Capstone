from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.stage_redshift import (StageToRedshiftOperator)
from operators.load_fact import (LoadFactOperator)
from operators.load_dimension import (LoadDimensionOperator)
from operators.data_quality import (DataQualityOperator)
from operators.data_clean import (DataCleanOperator)


from helpers.sql_queries import SqlQueries
import logging
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'AKY',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

## DAG schedule is set to none so as to trigger on demand via airflow
dag = DAG('etl_immigration_dag',
          default_args=default_args,
          description='Load and transform data into Redshift with Airflow',
          schedule_interval=None
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


# Stage S3 immigration parquet data to Redshift 
stage_immigration_to_redshift = StageToRedshiftOperator(
    task_id='Stage_immigration',
    table='fact_immigration',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend-capstone-aky',
    s3_key='sas_data',
    copy_option="FORMAT AS PARQUET",
    truncate=True,
    dag=dag
)

# Stage S3 demographic csv data to Redshift 
stage_demographics_to_redshift = StageToRedshiftOperator(
    task_id='Stage_demographics',
    table='dim_demographics_table',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend-capstone-aky',
    s3_key='dim_data/us-cities-demographics.csv',
    copy_option="FORMAT AS CSV DELIMITER ';' IGNOREHEADER 1",
    truncate=True,
    dag=dag
)

load_i94model_dimension_table = LoadDimensionOperator(
    task_id='Load_i94model_dim_table',
    table='dim_i94model_table',
    dim_value='i94model',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend-capstone-aky',
    s3_key='dim_data/I94_SAS_Labels_Descriptions.SAS',
    truncate=True,
    dag=dag
)

load_i94addrl_dimension_table = LoadDimensionOperator(
    task_id='Load_i94addrl_dim_table',
    table='dim_i94addrl_table',
    dim_value='i94addrl',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend-capstone-aky',
    s3_key='dim_data/I94_SAS_Labels_Descriptions.SAS',
    truncate=True,
    dag=dag
)

load_i94prtl_dimension_table = LoadDimensionOperator(
    task_id='Load_i94prtl_dim_table',
    table='dim_i94prtl_table',
    dim_value='i94prtl',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend-capstone-aky',
    s3_key='dim_data/I94_SAS_Labels_Descriptions.SAS',
    truncate=True,
    dag=dag
)

load_i94visal_dimension_table = LoadDimensionOperator(
    task_id='Load_i94visal_dim_table',
    table='dim_i94visal_table',
    dim_value='I94VISA',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend-capstone-aky',
    s3_key='dim_data/I94_SAS_Labels_Descriptions.SAS',
    truncate=True,
    dag=dag
)

load_i94cntyl_dimension_table = LoadDimensionOperator(
    task_id='Load_i94cntyl_dim_table',
    table='dim_i94cntyl_table',
    dim_value='i94cntyl',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend-capstone-aky',
    s3_key='dim_data/I94_SAS_Labels_Descriptions.SAS',
    truncate=True,
    dag=dag
)


data_clean_addrl = DataCleanOperator(
    task_id='Data_clean_addrl',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.data_clean_addrl,
    dag=dag
)

data_clean_cntyl = DataCleanOperator(
    task_id='Data_clean_cntyl',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.data_clean_cntyl,
    dag=dag
)

data_clean_prtl = DataCleanOperator(
    task_id='Data_clean_prtl',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.data_clean_prtl,
    dag=dag
)

data_clean_fact = DataCleanOperator(
    task_id='Data_clean_fact',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.data_clean_fact,
    dag=dag
)

# Row count of model table must be > 0
run_quality_model_checks = DataQualityOperator(
    task_id='Run_data_quality_model_checks',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.model_table_count_check,
    gt_result_expectation=0,
    dag=dag
)

# Row count of addrl table must be > 0
run_quality_addrl_checks = DataQualityOperator(
    task_id='Run_data_quality_addrl_checks',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.addrl_table_count_check,
    gt_result_expectation=0,
    dag=dag
)

# Row count of cntyl table must be > 0
run_quality_cntyl_checks = DataQualityOperator(
    task_id='Run_data_quality_cntyl_checks',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.cntyl_table_count_check,
    gt_result_expectation=0,
    dag=dag
)

# Row count of prtl table must be > 0
run_quality_prtl_checks = DataQualityOperator(
    task_id='Run_data_quality_prtl_checks',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.prtl_table_count_check,
    gt_result_expectation=0,
    dag=dag
)

# Row count of cntyl table must be > 0
run_quality_visal_checks = DataQualityOperator(
    task_id='Run_data_quality_visal_checks',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.visal_table_count_check,
    gt_result_expectation=0,
    dag=dag
)

# Row count of fact table must be > 0
run_quality_fact_checks = DataQualityOperator(
    task_id='Run_data_quality_fact_checks',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.fact_table_count_check,
    gt_result_expectation=0,
    dag=dag
)

# Row count of fact table must be > 0
run_quality_demographics_checks = DataQualityOperator(
    task_id='Run_data_quality_demographics_checks',
    redshift_conn_id='redshift',
    sql_txt=SqlQueries.demographics_table_count_check,
    gt_result_expectation=0,
    dag=dag
)


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


## GRAPH ##


start_operator >> stage_immigration_to_redshift
start_operator >> stage_demographics_to_redshift

start_operator >> load_i94addrl_dimension_table
start_operator >> load_i94cntyl_dimension_table
start_operator >> load_i94model_dimension_table
start_operator >> load_i94prtl_dimension_table
start_operator >> load_i94visal_dimension_table

stage_immigration_to_redshift >> data_clean_fact
data_clean_fact >> run_quality_fact_checks
run_quality_fact_checks >> end_operator

stage_demographics_to_redshift >> run_quality_demographics_checks
run_quality_demographics_checks >> end_operator

load_i94addrl_dimension_table >> data_clean_addrl
load_i94cntyl_dimension_table >> data_clean_cntyl
load_i94prtl_dimension_table >> data_clean_prtl

data_clean_addrl >> run_quality_addrl_checks
data_clean_cntyl >> run_quality_cntyl_checks

run_quality_addrl_checks >> end_operator
run_quality_cntyl_checks >> end_operator

load_i94model_dimension_table >> run_quality_model_checks
run_quality_model_checks >> end_operator

data_clean_prtl >> run_quality_prtl_checks
run_quality_prtl_checks >> end_operator

load_i94visal_dimension_table >> run_quality_visal_checks
run_quality_visal_checks >> end_operator


