CREATE TABLE public.fact_immigration (
	cicid FLOAT NULL, 
 i94yr FLOAT NULL, 
 i94mon FLOAT NULL, 
 i94cit FLOAT NULL, 
 i94res FLOAT NULL, 
 i94port NVARCHAR(MAX) NULL, 
 arrdate FLOAT NULL, 
 i94mode FLOAT NULL, 
 i94addr NVARCHAR(MAX) NULL, 
 depdate FLOAT NULL, 
 i94bir FLOAT NULL, 
 i94visa FLOAT NULL, 
 count FLOAT NULL, 
 dtadfile NVARCHAR(MAX) NULL, 
 visapost NVARCHAR(MAX) NULL, 
 occup NVARCHAR(MAX) NULL, 
 entdepa NVARCHAR(MAX) NULL, 
 entdepd NVARCHAR(MAX) NULL, 
 entdepu NVARCHAR(MAX) NULL, 
 matflag NVARCHAR(MAX) NULL, 
 biryear FLOAT NULL, 
 dtaddto NVARCHAR(MAX) NULL, 
 gender NVARCHAR(MAX) NULL, 
 insnum NVARCHAR(MAX) NULL, 
 airline NVARCHAR(MAX) NULL, 
 admnum FLOAT NULL, 
 fltno NVARCHAR(MAX) NULL, 
 visatype NVARCHAR(MAX) NULL
);

CREATE TABLE public.dim_demographics_table (
	city NVARCHAR(MAX) NULL, 
    State NVARCHAR(MAX) NULL, 
    Median_Age FLOAT NULL, 
    male_population INT,
    female_population INT,
    total_population INT,
    number_of_veterans INT,
    foreign_born INT,
    average_household_size FLOAT,
    state_code NVARCHAR(MAX) NULL,
    race NVARCHAR(MAX) NULL,
    count INT
);

CREATE TABLE public.dim_i94addrl_table (
	i94addr VARCHAR(256) NOT NULL,  
    addr_value VARCHAR(256) NULL
);

CREATE TABLE public.dim_i94model_table (
	i94mode FLOAT NOT NULL,  
    mode_value VARCHAR(256) NULL
);

CREATE TABLE public.dim_i94cntyl_table (
	i94cnty VARCHAR(256) NOT NULL, 
    cnty_value VARCHAR(256) NULL
);

CREATE TABLE public.dim_i94prtl_table (
	i94prt VARCHAR(256) NOT NULL, 
    prt_value VARCHAR(256) NULL
);

CREATE TABLE public.dim_i94visal_table (
	i94visa VARCHAR(256) NOT NULL, 
    visa_value VARCHAR(256) NULL
);

