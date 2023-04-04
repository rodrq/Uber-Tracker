# Uber-Tracker

query_to_local:
    
    - For data analysis purposes.
    - Set .env file with your AWS credentials and load it (from dotenv import load_dotenv then load_dotenv()).
    - Initialize UberFaresQuery object with 'table_name, month, year, partition_key, aws_region' as args.
    - yourquery.tocvs_fares_in_month() writes a csv per day inside 'data' folder. 
    
