import requests
import boto3
import os
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tracker_db')

def get_price():
    url = "https://m.uber.com/graphql"
    payload = json.dumps({
        "operationName": "Products",
        "variables": {
            "includeClassificationFilters": False,
            "destinations": [
                {
                    "latitude": float(os.environ.get("DESTINO_LAT")),
                    "longitude": float(os.environ.get("DESTINO_LON"))
                }
            ],
            "fallbackTimezone": os.environ.get("TIMEZONE"),
            "pickup": {
                "latitude": float(os.environ.get("PICKUP_LAT")),
                "longitude": float(os.environ.get("PICKUP_LON"))
            },
            "targetProductType": None
        },
        "query": "query Products($destinations: [InputCoordinate!]!, $fallbackTimezone: String, $includeClassificationFilters: Boolean = false, $pickup: InputCoordinate!, $pickupFormattedTime: String, $targetProductType: EnumRVWebCommonTargetProductType) {\n  products(\n    destinations: $destinations\n    fallbackTimezone: $fallbackTimezone\n    includeClassificationFilters: $includeClassificationFilters\n    pickup: $pickup\n    pickupFormattedTime: $pickupFormattedTime\n    targetProductType: $targetProductType\n  ) {\n    ...ProductsFragment\n    __typename\n  }\n}\n\nfragment ProductsFragment on RVWebCommonProductsResponse {\n  classificationFilters {\n    ...ClassificationFiltersFragment\n    __typename\n  }\n  defaultVVID\n  productsUnavailableMessage\n  renderRankingInformation\n  tiers {\n    ...TierFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ClassificationFiltersFragment on RVWebCommonClassificationFilters {\n  filters {\n    ...ClassificationFilterFragment\n    __typename\n  }\n  hiddenVVIDs\n  standardProductVVID\n  __typename\n}\n\nfragment ClassificationFilterFragment on RVWebCommonClassificationFilter {\n  currencyCode\n  displayText\n  fareDifference\n  icon\n  vvid\n  __typename\n}\n\nfragment TierFragment on RVWebCommonProductTier {\n  products {\n    ...ProductFragment\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment ProductFragment on RVWebCommonProduct {\n  capacity\n  cityID\n  currencyCode\n  description\n  detailedDescription\n  discountPrimary\n  displayName\n  estimatedTripTime\n  etaStringShort\n  fare\n  hasPromo\n  hasRidePass\n  id\n  isAvailable\n  meta\n  preAdjustmentValue\n  productImageUrl\n  productUuid\n  reserveEnabled\n  __typename\n}\n"
})

    headers = {
        'accept': '*/*',
        'cookie': os.environ.get("SID") + os.environ.get("CSID"),
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-csrf-token': 'x',
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        fare = json.loads(response.text)['data']['products']['tiers'][0]['products'][0]['fare'][4:]
        return fare
    except:
        return 'Request error'

def lambda_handler(event, context):
    response = {'date':datetime.now().strftime('%y-%m-%d'), 'time': datetime.now().strftime('%H:%M'), 'price': get_price()}
    table.put_item(Item=response)
    return ('Item added to DynamoDB:', response)