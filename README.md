# Capstone Project
### Data Engineering Capstone Project

#### Project Summary
This project follows the Udacity proivided project, which will combine various datasets. I have chosen to combine data on US immigration with supplimentary data based on US City demographics. It is also combined with dimensional data enriched from a dictionary file. This results in a small star schema data model which can be used to analyse immigration trends over the period of the data provided.
The immigration data used has more than one million rows and so consideration is given to the efficiency of loading this data into the star schema. 

The project follows the following steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

### Step 1: Scope the Project and Gather Data

#### Scope 
The scope of this project will be to gather and describe immigration data with supporting dimensional data, so that a small star schema based data warehouse can be created. The end solution and purpose of the final data model would be that this small data warehouse could be used to query immigration trends and summaries based around demographics and other dimensions such as by country or port or mode of travel, etc. 

The data used in this project is as follows:
- I94 Immigration Data: This data comes from the US National Tourism and Trade Office (parquet files)
- The data disctionary data for the above I94 Immigration Data data (sas file)
- U.S. City Demographic Data: This data comes from OpenSoft (csv file)

The tools used in the project are:
- Jupyter notebook for structuring and performing the data analysis, exploration and assessment. Also this was used for defining and planning the pipelines necessary to take the raw data and transform it into the star schema data warehouse. The notebook was a good way planning the porject as well as being able to write small code snippets that would contribute to the end solution. Please see "Capstone Project.ipynb"
- Airflow to orchestrate the ETL pipeline. This tool is excellent at coordinating the tasks involved in the ETL pipeline and is justified by also allowing for several tasks being able to be executed in parallel at once.
- Python to code the ETL process
- VS Studio Code to help write the ETL progress. This tool helped me write the pythin code, especially with syntax highlighting
- Anaconda local installation for the development environment. This environment worked alongside my jupyter notebook.
- Docker to test the airflow pipeline locally. This provided the runtime environment for my local airflow installation, where I could see all the logs generated, etc.
- AWS S3 to host the raw input data. Since the fact data is a large dataset, it seemed best to me to store it on S3 to allow for it to be staged directly to Redshift with minimal delay, Supporting files are also stored here.
- AWS Redshift to host the star schema data warehouse. This is justified by its scalability and ease of use. If it was necessary to process a larger amount of data then Redshift can be scaled up by adding more nodes.

#### Describe and Gather Data 
 
Dimension data is going to come from the I94_SAS_Labels_Descriptions.SAS file  
i94cntyl / i94cit / i94res - dimension data - Countries   
i94prtl - port within state   
i94mode - mode of travel   
i94addrl - states   
i94visa - travel visa   

Further dimension data is going to come from the us-cities-demographics.csv file. This data is grouped by State, City and Race. It contains population data broken down at this level. 

See the Jupyter Notebook for the Capsone Project contained within this repository for a breakdown of the analysis performed.

### Step 2: Explore and Assess the Data
#### Explore the Data 
#### Cleaning Steps
Steps necessary to clean the data (Cleaning will be performed in the ETL pipeline)

##### Dimension Data:

i94cntyl / i94cit / i94res - dimension data - Countries - remove "INVALID", "Collapsed","No Country Code"

$i94prtl - port within state - remove "Collapsed", "No PORT Code"

i94mode - mode of travel - no cleaning identified

i94addrl - states - remove "All Other Codes"

i94visa - travel visa - no cleaning identified

us-cities-demographics - Data is grouped by state, city and race. State is in the fact table, so this will be a foreign key on the fact table.  Other than that, the data looks complete with no cleaning identified

#### Cleaning of Fact data
It can be notcied that gender is either missing or is not "M" or "F" (i.e. is unknown). Since gender is required for demographics analysis, these entries will be dropped. This data will be dropped post loading into the redshift table because due to the size, I do not want to load this data into pandas dataframes. These entries will be 'cleaned' post loading to the fact table which I believe to be the most efficient. It would be possible to add further cleaning steps on the fact data at a later time, such as removing entries which have a missing state. 

### Step 3: Define the Data Model
#### 3.1 Conceptual Data Model
The purpose of the final data model is so that reports or a dashboard can be run to get statistics based on the following groupings:  
    1. Mode of Travel  
    2. State  
    3. Country  
    4. Travel Visa  
    5. Port  
    
An extra dimension is also added based upon state demographics. This will allow for the further construction of state based statistics with a demographic element, such as male, female and total population and foreign born. This could be used to find demographic correlations in the data such as percentages of state immigration based upon population.   

![model](https://github.com/andrewkendallyoung/Capstone/assets/122558520/dca0f197-0ad6-4114-853c-8c732613ec19)

#### 3.2 Mapping Out Data Pipelines
These are the steps necessary to pipeline the data into my chosen data model.

1. Stage immigration parquet files from S3 into fact_immigration table
2. In parallel with the above, load the dimension tables by transforming the data in the dictionary file: I94_SAS_Labels_Descriptions.SAS 
3. Once the fact and dimension tables are loaded, perform data cleansing processes (in SQL) on them
4. Once all data cleansing processes are complete, perform data quality checks on the fact and dimension tables
5. The successful end of the pipeline will be when all data quality checks are passed. A failure of a data quality check will result in the failure of the DAG step

The steps will be orchestrated to run by airflow in a DAG.  

### !! Prerequisits BEFORE running the DAG in Airflow !!
- Immigration parquet files are to be uploaded into an S3 bucket in advance  
- The files "us-cities-demographics.csv" and I94_SAS_Labels_Descriptions.SAS supporting files are also be uploaded and made available in the same S3 bucket   
- **I have already uploaded these files into the following public buckets:**
  - s3://dacity-dend-capstone-aky/sas_data   
  - s3://dacity-dend-capstone-aky/dim_data  
- The following parameters should be set in Airflow .. Connections  
  - aws_credentials (Type Amazon Web Services). The login and password are the user authorised to access S3 and Redshift.
  - redshift (Type postgres). Specifying the host endpoint of the redshift cluster along with the aws user, password and port number.
- On the redshift cluster, before running the DAG, pre-create the schema physical data model by running: **create_immg_tables.sql**


### Step 4: Run Pipelines to Model the Data 
#### 4.1 Create the data model
Run the DAG pipeline in airflow 

![etl_immigration_dag](https://github.com/andrewkendallyoung/Capstone/assets/122558520/32cb85c5-7e54-4680-a153-ac9e34e7ea08)


#### See code in this repository

dags/etl_immigration_dag.py  

plugins/helpers/sql_queries.py  
plugins/operators/data_clean.py  
plugins/operators/data_quality.py  
plugins/operators/load_dimensions.py  
plugins/operators/stage_redshift.py  

#### 4.2 Data Quality Checks
* Seven data quality checks are run, one for each loaded table, to ensure none are empty. If any empty tables are found then the DAG step will fail. 
 

#### 4.3 Data dictionary 
The Data Dictionary is included in the Jupyter Notebook.

#### Step 5: Project Write Up Summary
* The rationale for the choice of tools and technologies for the project is stated above in section 1.
* The current DAG schedule is set to "none". This is so that it can be run on demand with a manual trigger. The data could be updated on an hourly or daily schedule. If this is the case then the truncate flags on the fact data should be set to "False", so that the data is appended and the schedule interval would be set to '@hourly'. It would not be necessary to refresh the dimension data unless it changes. 
* How I would approach the problem differently under the following scenarios:
 * The data was increased by 100x. In this case I would not change anything about the process I developed except I would check the monitoring tools within AWS Redshift to see if the resources (CPU, etc) are over utilised. If this is the case I would add a node to the cluster to expand the processing (scale out) or increase the cluster type power (scale up). This would be repeated until the solution was scaled properly.  
 * The data populates a dashboard that must be updated on a daily basis by 7am every day. I would run the DAG on a daily schedule with a start time that would mean the DAG would complete by 7am. 
 * The database needed to be accessed by 100+ people. In this case there would be increased pressure to the database engine. I would look to scale out or scale up the Redshift Cluster in order to meet this demand.
