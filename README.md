# Uber-Tracker
Project to track Uber's fare to my gf's house. Since I live in a country with high inflation, it's hard to know when a fare is high because of Uber's dynamic pricing (supply and demand) or just because it increased as everything in the economy. 

Coded with Python. Using requests, FastAPI, AWS (Lambda, DynamoDB, API Gateway) and a microservice approach. 

fare_request:

    - Gets price with http request using requests library.
    - Connects to my DynamoDB table with 'date' as partition key, and 'time' as sort key. 
    - Runs every minute with an AWS EventBridge (fixed rate 1 minute) and puts item into the table. 
    - Item being {'date': now as y-m-d, 'time': now as %H:%M, 'price': get_price()}
    
    - Needs csid and sid from your Uber session, input pickup and destination coordinates and timezone as Lambda environment variables. 
    - csid and sid expire after a month.

api:

    - FastAPI API with two read-only functions. One queries all the fares in a day, the other a fare from a certain hour.
    - 404 if fare not found.
    - Connects to DynamoDB with Boto3. 
    - Setup with API Gateway lambda trigger and lambda_proxy integration as method and resource. 


query_to_local:
    
    - For data analysis purposes.
    - Set .env file with your AWS credentials and load it (from dotenv import load_dotenv then load_dotenv()).
    - Initialize UberFaresQuery object with 'table_name, month, year, partition_key, aws_region' as args.
    - yourquery.tocvs_fares_in_month() writes a csv per day inside 'data' folder. 
    

Get all fares from month:

![image](https://user-images.githubusercontent.com/84244902/229661052-357f20a0-742b-4930-8044-493b25f17263.png)
    
![image](https://user-images.githubusercontent.com/84244902/229658288-d7e03c6a-15ff-4ac5-b1a7-60bd03093410.png)

Get fare from certain hour:

![image](https://user-images.githubusercontent.com/84244902/229661211-f7dbc0ef-8ee8-4fc5-8d4b-d9ccf5425139.png)

![image](https://user-images.githubusercontent.com/84244902/229661239-a73a4d6a-4787-437a-b969-cadc235b6cd4.png)
