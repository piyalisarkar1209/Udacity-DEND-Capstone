from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
#import sql_statements_cs

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('udac_capstone_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@daily',
          catchup=False
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_task = PostgresOperator(
    task_id="create_tables",
    dag=dag,
    postgres_conn_id="redshift",
    sql='create_tables_cs.sql'
)

stage_listings_to_redshift = StageToRedshiftOperator(
    task_id='Stage_listings_table',
    dag=dag,
    table="staging_listing",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstoneprojectpiyali",
    s3_key="listings.csv",
    region="us-west-2",
    extra_params= ''
#    extra_params="FORMAT AS CSV 's3://capstoneprojectpiyali/listings.csv'"
)

stage_calendar_to_redshift = StageToRedshiftOperator(
    task_id='Stage_calendar_table',
    dag=dag,
    table="staging_calendar",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstoneprojectpiyali",
    s3_key="calendar.csv",
    region="us-west-2",
    extra_params= ''
#    extra_params="JSON 'auto' COMPUPDATE OFF"
)

load_listing_dimension_table = LoadDimensionOperator(
    task_id='Load_listing_dim_table',
    dag=dag,
    table='dim_listing',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql_stmt=SqlQueries.dim_listing_table_insert
)

load_host_dimension_table = LoadDimensionOperator(
    task_id='Load_host_dim_table',
    dag=dag,
    table='dim_host',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql_stmt=SqlQueries.dim_host_table_insert
)

load_district_dimension_table = LoadDimensionOperator(
    task_id='Load_district_dim_table',
    dag=dag,
    table='dim_district',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql_stmt=SqlQueries.dim_district_table_insert
)

load_neighbourhood_dimension_table = LoadDimensionOperator(
    task_id='Load_neighbourhood_dim_table',
    dag=dag,
    table='dim_neighbourhood',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql_stmt=SqlQueries.dim_neighbourhood_table_insert
)

load_property_dimension_table = LoadDimensionOperator(
    task_id='Load_property_dim_table',
    dag=dag,
    table='dim_property',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql_stmt=SqlQueries.dim_property_table_insert
)

load_date_dimension_table = LoadDimensionOperator(
    task_id='Load_date_dim_table',
    dag=dag,
    table='dim_date',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql_stmt=SqlQueries.dim_date_table_insert
)


load_f_neighbourhood_listing_table = LoadFactOperator(
    task_id='Load_f_neighbourhood_listing_fact_table',
    dag=dag,
    table='f_neighbourhood_listing',
    redshift_conn_id="redshift",
    load_sql_stmt=SqlQueries.f_neighbourhood_listing_insert
)

load_f_listing_table = LoadFactOperator(
    task_id='Load_f_listing_fact_table',
    dag=dag,
    table='f_listing',
    redshift_conn_id="redshift",
    load_sql_stmt=SqlQueries.f_listing_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    dq_checks=[
        { 'check_sql': 'SELECT COUNT(*) FROM public.f_neighbourhood_listing WHERE id_date IS NULL', 'expected_result': 0 }, 
        { 'check_sql': 'SELECT COUNT(DISTINCT "district_id") FROM public.dim_district', 'expected_result': 5 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.dim_host WHERE host_id IS NULL', 'expected_result': 0 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.dim_property WHERE property_type IS NULL', 'expected_result': 0 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.dim_listing WHERE price IS NULL', 'expected_result': 0 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.dim_district WHERE district IS NULL', 'expected_result': 0 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.f_neighbourhood_listing nl LEFT OUTER JOIN public.dim_neighbourhood n ON nl.neighbourhood = n.neighbourhood WHERE n.neighbourhood IS NULL', \
         'expected_result': 0 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.f_listing l LEFT OUTER JOIN public.dim_property p ON l.id = p.listing_id WHERE p.listing_id IS NULL', \
         'expected_result': 0 }
    ],
    redshift_conn_id="redshift"
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

#
# Tasks ordering
#

start_operator >> create_tables_task

create_tables_task >> stage_listings_to_redshift
create_tables_task >> stage_calendar_to_redshift

create_tables_task >> load_date_dimension_table

stage_listings_to_redshift >> load_listing_dimension_table 
stage_calendar_to_redshift >> load_listing_dimension_table

stage_listings_to_redshift >> load_host_dimension_table
stage_calendar_to_redshift >> load_host_dimension_table

stage_listings_to_redshift >> load_district_dimension_table
stage_calendar_to_redshift >> load_district_dimension_table

stage_listings_to_redshift >> load_property_dimension_table
stage_calendar_to_redshift >> load_property_dimension_table

load_district_dimension_table >> load_neighbourhood_dimension_table

stage_listings_to_redshift >> load_f_neighbourhood_listing_table
stage_calendar_to_redshift >> load_f_neighbourhood_listing_table
load_date_dimension_table >> load_f_neighbourhood_listing_table
load_neighbourhood_dimension_table >> load_f_neighbourhood_listing_table
load_neighbourhood_dimension_table >> load_f_listing_table
load_property_dimension_table >> load_f_listing_table
stage_listings_to_redshift >> load_f_listing_table

load_listing_dimension_table >> run_quality_checks
load_host_dimension_table >> run_quality_checks
load_district_dimension_table >> run_quality_checks
load_property_dimension_table >> run_quality_checks
load_f_neighbourhood_listing_table >> run_quality_checks
load_f_listing_table >> run_quality_checks


run_quality_checks >> end_operator

#load_listing_dimension_table  >> end_operator
#load_host_dimension_table >>  end_operator
#load_property_dimension_table >>  end_operator
#load_neighbourhood_dimension_table >> end_operator
#load_date_dimension_table >> end_operator
#load_f_neighbourhood_listing_table >> end_operator


