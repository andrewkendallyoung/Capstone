import pandas as pd
from sqlalchemy import create_engine
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.base_hook import BaseHook
from airflow.hooks.S3_hook import S3Hook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'


    trunc_sql = """
        TRUNCATE TABLE {}
        ;
    """

    @apply_defaults
    def __init__(self,
                 # operators params (with defaults) 
                 table="",
                 dim_value="",
                 redshift_conn_id="",
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="",
                 truncate=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Parameter Mappings
        self.table = table
        self.dim_value = dim_value
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.truncate = truncate 


    def execute(self, context):

        """
        Operator to get, clean then load dimension table from a dictionary file stored in an AWS S3 bucket
        Parameters:
            table = table name to load
            dim_value = dimension value to find in dictionary file
            redshift_conn_id = redshift connection id defined in airflow
            aws_credentials_id = credentials for accessing the file on S3
            s3_bucket: first part of the s3 bucket name 
            s3_key: next part of s3 bucket name (including dictionary file name) 
            truncate = first do a truncate (true) or not (false)
        
        """
        self.log.info(f"Begin Loading {self.table} dim table")

        # First read dictionary file and search for given dimension data

        s3 = S3Hook(self.aws_credentials_id)
        self.log.info('Reading S3: s3://{}/{}'.format(self.s3_bucket, self.s3_key))

        file_content = s3.read_key(self.s3_key, self.s3_bucket)
        self.log.info('File has {} characters'.format(len(file_content)))

        file_lines = file_content.splitlines()

        value_found = False
        key_codes_list = []
        key_values_list = []

        self.log.info('Parsing File')
        for line in file_lines:
            if self.dim_value in line:
                value_found=True
            if value_found and '=' in line:
                key_code, val = line.split('=')
                key_code = key_code.strip()
                key_val = val.strip()
                key_val = key_val.replace(";","")
                key_val = key_val.replace("'","")
                key_code = key_code.replace("'","")
                key_codes_list.append(key_code)
                key_values_list.append(key_val)
                if ';' in line:
                    break
            else:
                if value_found and ';' in line:
                    break    
        
        self.log.info('Completed Parsing File')

        df = pd.DataFrame(list(zip(key_codes_list,key_values_list)))
        ## df.columns = ['key_code', 'key_value']
        df = df.astype(str)

        ## Clean dimension data of any spurious entries before loading into the database  
        #df = df [df["key_value"].str.contains("No Country Code") == False]
        #df = df [df["key_value"].str.contains("Collapsed") == False]
        #df = df [df["key_value"].str.contains("INVALID") == False]
        #df = df [df["key_value"].str.contains("No PORT Code") == False]
        #df = df [df["key_value"].str.contains("All Other Codes") == False]
         
        # Connect to Redshift database
        pg_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.truncate:
            self.log.info(f"Truncating {self.table} dim table")
            redshift_sql = LoadDimensionOperator.trunc_sql.format (self.table)
            pg_hook.run(redshift_sql)

        # Convert data frame to tuple, ready for loading 
        data_tuple = [tuple(r) for r in df.to_numpy()]    
        
        # Insert dimension data into table
        pg_hook.insert_rows(self.table, data_tuple)
        
        
        self.log.info(f"End Loading {self.table} dim table")
