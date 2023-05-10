from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        {}
        ;
    """

    trunc_sql = """
        TRUNCATE TABLE {}
        ;
    """

##  REGION AS '{}'
    
    @apply_defaults
    def __init__(self,
                 ### Operator params (with defaults) 
                 table="",
                 redshift_conn_id="",
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="",
                 copy_option="",
                 truncate=True,
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Parameter Mappings
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.copy_option= copy_option
        self.truncate = truncate
        

    def execute(self, context):
        """
        Operator to perform the data staging from a given S3 bucket to a given redshift table
        Parameters:
            table: the redshift table to be loaded
            redshift_conn_id: redshift connection id defined in airflow
            aws_credentials_id: the AWS connection id as defined in airflow
            s3_bucket: first part of the s3 bucket name 
            s3_key: next part of s3 bucket name 
            copy_option: any extra parameters needed for the S3 COPY command, such as FORMAT AS .. 
            truncate = first do a truncate (true) or not (false) 
            
        
        """
       
        self.log.info(f"Begin Data Staging from S3 to Redshift: {self.table} table")
        
        aws_hook = AwsHook(self.aws_credentials_id)
        aws_credentials = aws_hook.get_credentials()
        pg_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Truncate table if required
        if self.truncate:
            self.log.info(f"Truncating {self.table} dim table")
            redshift_sql = StageToRedshiftOperator.trunc_sql.format (self.table)
            pg_hook.run(redshift_sql)

        # Stage S3 files
        from_path = f"s3://{self.s3_bucket}/{self.s3_key}"

        redshift_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            from_path,
            aws_credentials.access_key,
            aws_credentials.secret_key,
            self.copy_option
        )
        self.log.info(f"Executing: '{redshift_sql}'")
        pg_hook.run(redshift_sql)
        self.log.info(f"End Data Staging from S3 to Redshift: {self.table} table")

