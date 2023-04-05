import requests
import datetime
import csv
import json

URL = 'your_api_url'

class UberFareQuery:
    def __init__(self, date:str):
        self.date = date
        self.url = f"{URL}/get-fare/"

    def api_request(self, date):
        response = requests.get(self.url + date)
        try:
            data = json.loads(response.text)
        except:
            raise Exception('No data')
        return data

    def format_date(self):
        formated_date = datetime.datetime.strptime(self.date, '%y-%m-%d')
        return formated_date
    
    def list_days_in_month(self):
        date = self.format_date()
        date = date.replace(day=28)
        #Hardcoded february because leap years and being the shortest month makes my code buggy.
        if date.month == 2:
            days = 28
        #Gets amount of days in month
        else:
            next_month = date + datetime.timedelta(days=4)
            last_day_of_month = (next_month - datetime.timedelta(next_month.day)).day
            days = [n+1 for n in range(last_day_of_month)]
        return days
    
    def format_days_in_month(self):
        days = self.list_days_in_month()
        date = self.format_date()
        month, year = date.month, date.year
        dates = [(datetime.datetime(year, month, n)).strftime('%y-%m-%d') for n in days]
        return dates
    

    def daily_csv_per_month(self):
        dates = self.format_days_in_month()
        for date in dates: 
            data = self.api_request(date)
            with open(f'/data/{date}.csv', 'a') as csvf:
                writer = csv.writer(csvf)
                writer.writerow(['Hour', 'Price'])
                for n in data:
                    time = n['time']
                    price = (n['price'].replace(',' , ''))[:-3] 
                    writer.writerow([time, price])
                print(f'Fetched {date} data')
        print('Done')



if __name__ == '__main__':
    obj = UberFareQuery('23-03-01')
    obj.daily_csv_per_month()


