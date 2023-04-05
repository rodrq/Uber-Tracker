import requests


url = API_URL

#This is super simple because I didn't set any authentication. 

def request_fare(endpoint:str):
    concat_url = f"{url}/get-fare/{endpoint}"
    response = requests.get(concat_url)
    data = response.text
    return print(data)



if __name__ == '__main__':
    fares=request_fare('%y-%m-%d')
    for n in fares:
        #Something
        pass


