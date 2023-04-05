# Uber-Tracker


- FastAPI API with two read-only functions. One queries all the fares in a day, the other a fare from a certain hour.
- 404 if fare not found.
- Connects to DynamoDB with Boto3. 
- Setup with API Gateway lambda trigger and lambda_proxy integration as method and resource. 


Get all fares from month:

![image](https://user-images.githubusercontent.com/84244902/229661052-357f20a0-742b-4930-8044-493b25f17263.png)
    
![image](https://user-images.githubusercontent.com/84244902/229658288-d7e03c6a-15ff-4ac5-b1a7-60bd03093410.png)

Get fare from certain hour:

![image](https://user-images.githubusercontent.com/84244902/229661211-f7dbc0ef-8ee8-4fc5-8d4b-d9ccf5425139.png)

![image](https://user-images.githubusercontent.com/84244902/229661239-a73a4d6a-4787-437a-b969-cadc235b6cd4.png)
