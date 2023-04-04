# Uber-Tracker

fare_request:

    - Gets price with http request using requests library.
    - Connects to my DynamoDB table with 'date' as partition key, and 'time' as sort key. 
    - Runs every minute with an AWS EventBridge (fixed rate 1 minute) and puts item into the table. 
    - Item being {'date': now as y-m-d, 'time': now as %H:%M, 'price': get_price()}
    
    - Needs csid and sid from your Uber session, input pickup and destination coordinates and timezone as Lambda environment variables. 
    - csid and sid expire after a month.

