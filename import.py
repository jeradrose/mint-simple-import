import csv
import datetime
from http.client import OK
import json
import requests
import time

# Config
UNCATEGORIZED_CATEGORY_ID =''
COOKIE_DATA = ''

# Open CSV
csv_data = csv.reader(open('transactions.csv','rU'))

next(csv_data) # Skip header row

for row in csv_data:
    # Read values in CSV
    # Update these to the proper 0-based column numbers
    # Also update if, for example, your amounts are a single positive/negative column
    date = (row[0]) 
    merchant = (row[1])
    debit = (row[2])
    credit = (row[3])

    # Convert date format from m/d/yyyy to yyyy-m-d
    # See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior for formats
    date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

    # Determine whether this transaction is an expense, and set amount (with negative sign, if applicable)
    # This logic will need to be updated if your amounts are a single positive/negative value
    if debit != '': 
        is_expense = 'true'
        amount = '-' + debit
    else: 
        is_expense = 'false'
        amount = credit

    # Build dictionary for data
    json_data = {
        'date': date,
        'description': merchant,
        'category': {  
            'id': UNCATEGORIZED_CATEGORY_ID,
            'name': None
        },
        'accountId': None,
        'amount': amount,
        'parentId': None,
        'type': 'CashAndCreditTransaction',
        'id': None,
        'isExpense': is_expense,
        'isPending': False,
        'isDuplicate': False,
        'tagData': None,
        'splitData': None,
        'manualTransactionType': 'CASH',
        'checkNumber': None,
        'isLinkedToRule': False,
        'shouldPullFromAtmWithdrawals': False
    }

    data_string = json.dumps(json_data)

    url = 'https://mint.intuit.com/pfm/v1/transactions'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'authorization': 'Intuit_APIKey intuit_apikey=prdakyresYC6zv9z3rARKl4hMGycOWmIb4n8w52r,intuit_apikey_version=1.0',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': str(len(data_string)),
        'Content-Type': 'application/json',
        'Cookie': COOKIE_DATA,
        'Host': 'mint.intuit.com',
        'Origin': 'https://mint.intuit.com',
        'Pragma': 'no-cache',
        'Referer': 'https://mint.intuit.com/transactions',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    response = requests.post(url, json=json_data, headers=headers)

    if response.status_code == 403:
        print("Unauthorized: make sure your cookie data is configured properly")
        break
    elif not response.ok:
        print("Resquest failed: " + response.content.decode("utf-8") )
        break

    # Force 1-second delay to prevent rate limiting
    time.sleep(1)
