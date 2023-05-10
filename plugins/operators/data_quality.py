from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#4000ff'
    ui_fgcolor = '#ffffff'

    @apply_defaults
    def __init__(self,
                 # operators params (with defaults) 
                 redshift_conn_id="",
                 sql_txt="",
                 gt_result_expectation=0,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Parameter Mappings
        self.redshift_conn_id = redshift_conn_id
        self.sql_txt = sql_txt
        self.gt_result_expectation = gt_result_expectation

    def execute(self, context):

        """
            Operator to perform a data quality check with a given SQL
            Parameters:
                redshift_conn_id = redshift connection id defined in airflow
                sql_text = the SQL text of the data quality check (result must be a number)
                gt_result_expectation = the result must be greater than this value 
        """

        self.log.info(f"Begin Data Quality Checking")
        pg_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        redshift_sql = self.sql_txt
        
        self.log.info(f"Executing: '{redshift_sql}'")
        
        rowcnt = pg_hook.get_records(redshift_sql)
        num_rows = rowcnt[0][0]

        if num_rows > self.gt_result_expectation:
            self.log.info(f"Data quality check PASSED. Actual count: {num_rows} greater than {self.gt_result_expectation}. ")
        else:
            raise ValueError(f"Data quality check FAILED. Actual count: {num_rows} NOT greater than {self.gt_result_expectation}. ")


        self.log.info(f"End Data Quality Checking")