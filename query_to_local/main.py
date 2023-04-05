import boto3
import os
import datetime
import csv


class UberFaresQuery:
    def __init__(self, table_name, month, year, partition_key, aws_region='us-east-2'):
        self.table_name = table_name
        self.month = month
        self.year = year
        self.partition_key = partition_key
        self.aws_region = aws_region
        self.table = self.session_setup()

    def session_setup(self):
        session = boto3.Session(
            aws_access_key_id=os.getenv('ACCESS_KEY'),
            aws_secret_access_key=os.getenv('SECRET_KEY'),
            region_name= self.aws_region
        )
        dynamodb = session.resource('dynamodb')
        table = dynamodb.Table(self.table_name)
        return table
    
    def query_by_sortkey(self, sort_key):
        query_params = {
            'KeyConditionExpression': '#key = :pk_value',
            'ExpressionAttributeNames': {
                '#key': self.partition_key
            }, 
            'ExpressionAttributeValues': {
                ':pk_value': sort_key
            }
        }
        response = self.table.query(**query_params)
        return response
    
    def list_of_days_in_month(self):
        date = datetime.datetime(2020, self.month, 28)
        next_month = date + datetime.timedelta(days=4)
        last_day_of_month = (next_month - datetime.timedelta(next_month.day)).day
        if self.month == 2:
            last_day_of_month = 28
            #February and leap years in general screws everything up so just hardcoded it.
        days = [n+1 for n in range(last_day_of_month)]
        return days
    
    def format_all_days_in_month(self):
        if self.year < 1000:
            raise Exception('Year arg needs 4 digits year')
        days = self.list_of_days_in_month()
        dates = [(datetime.datetime(self.year, self.month, n)).strftime('%y-%m-%d') for n in days]
        return dates
    
    def tocvs_fares_in_month(self):
        dates = self.format_all_days_in_month()
        for date in dates: 
            csvfile = f'data/{date}.csv'
            result = self.query_by_sortkey(date)
            if result['Count'] > 700:
                with open(csvfile, 'a') as csvf:
                    writer = csv.writer(csvf)
                    writer.writerow(['Hour', 'Price'])
                    for n in result['Items']:
                        time = n['time']
                        price = (n['price'].replace(',' , ''))
                        price = price[:-3]  
                        writer.writerow([time, price])
                    print(f'Fetched {date} data')
            else:
                print(f"Not fetching data from {date} because less than 50% filled or is in the future.")
        print('Done')


"""
if __name__ == '__main__':
    query = UberFaresQuery('tracker_db', 4, 2023, 'date')
    print(query.query_by_sortkey('23-04-02'))
"""

