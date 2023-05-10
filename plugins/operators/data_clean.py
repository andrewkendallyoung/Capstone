from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataCleanOperator(BaseOperator):

    ui_color = '#89DB59'

    @apply_defaults
    def __init__(self,
                 # operators params (with defaults) 
                 redshift_conn_id="",
                 sql_txt="",
                 *args, **kwargs):

        super(DataCleanOperator, self).__init__(*args, **kwargs)
        # Parameter Mappings
        self.redshift_conn_id = redshift_conn_id
        self.sql_txt = sql_txt

    def execute(self, context):

        """
            Operator to perform data cleaning
            Parameters:
                redshift_conn_id = redshift connection id defined in airflow
                sql_text = the SQL text of the data cleaning action (e.g. delete) 
                
        """

        self.log.info(f"Begin Data Cleaning")
        pg_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        redshift_sql = self.sql_txt
        
        self.log.info(f"Executing: '{redshift_sql}'")
        pg_hook.run(redshift_sql)

        self.log.info(f"End Data Cleaning")