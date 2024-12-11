import os.path
import json
import db_dtypes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.cloud import bigquery


# This function retrieves the number of distinct persons per date for the last N specified number of dates
# from the BigQuery dataset. It returns the results as a JSON string.
#
# Parameters:
# last_dates_count (int): The number of most recent dates to consider.
#
# Returns:
# str: A JSON string containing the number of distinct persons per date.
def get_persons_per_date(last_dates_count: int) -> str:
    client = bigquery.Client()
    query_job = client.query(
        f"""
        SELECT
            a.procedure_dat,
            count(DISTINCT a.person_id) as person_count
        FROM `bigquery-public-data.cms_synthetic_patient_data_omop.procedure_occurrence` a
        INNER JOIN (
                SELECT
                    DISTINCT procedure_dat
                FROM `bigquery-public-data.cms_synthetic_patient_data_omop.procedure_occurrence`
                ORDER BY procedure_dat DESC
                LIMIT {str(last_dates_count)}) b
            on a.procedure_dat = b.procedure_dat
        group by a.procedure_dat"""
    )

    return query_job.to_dataframe().to_json(orient='records', date_format='iso')


# This function retrieves the number of distinct persons and providers per date for a specified procedure type
# from the BigQuery dataset. It returns the results as a JSON string.
#
# Parameters:
# procedure_type (int): The concept ID of the procedure type to consider.
#
# Returns:
# str: A JSON string containing the number of distinct persons and providers per date for the specified procedure type.
def get_procedure_usage(procedure_type: int) -> str:
    client = bigquery.Client()
    query_job = client.query(
        f"""
        SELECT
            procedure_dat,
            count(DISTINCT person_id) as person_count,
            count(DISTINCT provider_id) as provider_count
        FROM `bigquery-public-data.cms_synthetic_patient_data_omop.procedure_occurrence`
        WHERE procedure_type_concept_id = {procedure_type}
        group by procedure_dat"""
    )

    return query_job.to_dataframe().to_json(orient='records', date_format='iso')



if __name__ == '__main__':
    # auth_service()
    # print(get_persons_per_date(10))
    print(get_procedure_usage(38000251))
