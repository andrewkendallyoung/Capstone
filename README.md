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
- Jupyter notebook for structuring and performing the data analysis, exploration and assessment. Also this was used for defining and planning the pipelines necessary to take the raw data and transform it into the star schema data warehouse. The notebook was a good way planning the porject as well as being able to write small code snippets that would contribute to the end solution.
- Airflow to orchestrate the ETL pipeline. This tool is excellent at coordinating the tasks involved in the ETL pipeline and is justified by also allowing for several tasks being able to be executed in parallel at once.
- Python to code the ETL process
- VS Studio Code to help write the ETL progress. This tool helped me write the pythin code, especially with syntax highlighting
- Anaconda local installation for the development environment. This environment worked alongside my jupyter notebook.
- Docker to test the airflow pipeline locally. This provided the runtime environment for my local airflow installation, where I could see all the logs generated, etc.
- AWS S3 to host the raw input data. Since the fact data is a large dataset, it seemed best to me to store it on S3 to allow for it to be staged directly to Redshift with minimal delay, Supporting files are also stored here.
- AWS Redshift to host the star schema data warehouse. This is justified by its scalability and ease of use. If it was necessary to process a larger amount of data then Redshift can be scaled up by adding more nodes.
- Excel to help visualise the data and look for data quality issues

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
Reason for choosing this model  
Fact data is immigration data. It will have the following dimensions, so that reports can be run to get statistics based on the following groupings:  
    1. Mode of Travel  
    2. State  
    3. Country  
    4. Travel Visa  
    5. Port  
    
An extra dimension is going to be added based upon state demographics. This will allow for the construction of state based statistics with a demographic element, such as male, female and total population and foreign born. This could be used to find demographic correlations in the data such as percentages of state immigration based upon population. 

#### 3.2 Mapping Out Data Pipelines
There are the steps necessary to pipeline the data into the chosen data model  

The steps will be run by airflow in a DAG.  

#### Prerequisits
- Immigration parquest files are to be uploaded into an S3 bucket in advance  
- The files "us-cities-demographics.csv" and I94_SAS_Labels_Descriptions.SAS supporting files will also be uploaded and made available in the same S3 bucket  

1. Stage immigration parquet files from S3 into fact_immigration table
2. In parallel with the above, load the dimension tables by transforming the data in the supporting files 
3. Once the fact and dimension tables are loaded, perform data cleansing processes (in SQL) on them
4. Once all data cleansing processes are complete, perform data quality checks on the fact and dimension tables
5. The successful end of the pipeline will be when all data quality checks are passed.

### Step 4: Run Pipelines to Model the Data 
#### 4.1 Create the data model
Build the data pipelines to create the data model.

#### See code in this repository

dags/etl_immigration_dag.py  

plugins/helpers/sql_queries.py  
plugins/operators/data_clean.py  
plugins/operators/data_quality.py  
plugins/operators/load_dimensions.py  
plugins/operators/stage_redshift.py  

#### 4.2 Data Quality Checks
Explain the data quality checks you'll perform to ensure the pipeline ran as expected. These could include:
 * Integrity constraints on the relational database (e.g., unique key, data type, etc.)
 * Unit tests for the scripts to ensure they are doing the right thing
 * Source/Count checks to ensure completeness
 
Run Quality Checks

#### 4.3 Data dictionary 
Create a data dictionary for your data model. For each field, provide a brief description of what the data is and where it came from. You can include the data dictionary in the notebook or in a separate file.

#### Step 5: Project Write Up Summary
* Clearly state the rationale for the choice of tools and technologies for the project.
* Propose how often the data should be updated and why.
* Write a description of how you would approach the problem differently under the following scenarios:
 * The data was increased by 100x.
 * The data populates a dashboard that must be updated on a daily basis by 7am every day.
 * The database needed to be accessed by 100+ people.
