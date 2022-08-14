# mint-simple-import
A simple import app for Mint.com.

This app loads transactions from a CSV file, and loops over them, importing them one at a time into Mint.com, using account data configured by a cookie value.

In order to run this, you will need to create a CSV with transactions you wish to load, and capture some data from a sample transaction you will create on Mint.com. This is explained in detail below.

Note that there are many similar import apps and articles written about how to do the same thing. However, at the time of this repo being created (mid 2022), these are all out of date and no longer work due to Mint changing their API.

**This app will work with the latest (2022) version of the Mint API (https://mint.intuit.com/transactions).**

## Prerequisites

- Requires Python 3 or greater.

- Requires the `requests` library:

      pip install requests

- Requires an account at Mint.com

## Instructions

### 1. Create the transactions.csv file

Using `transactions.csv` as an example, create transactions either manually, or from a downloaded file from your bank. If the format of the file from your bank is different, you will either need to manipulate the file to match the format of the sample file, or you will need to modify the code to map the data correctly.

### 2. Grab the cookie & category data for your account from Mint.com

The app needs to simulate activity from your account. To do this, you will need to grab the cookie data from your account.

1. Log in to Mint.com with your account

2. Open [devtools](https://balsamiq.com/support/faqs/browserconsole/) in your browser, and click the network tab

3. Manually add a new transaction in Mint; Be sure to select the root "Uncategorized" category

4. After adding the new transaction, look for a request in the network tab named `transactions` -- this is the POST request that was made when you added your transaction, which is what this app will simulate

5. From the `transactions` request:

   - Copy *all* of the content from the `Cookie` header and paste this as the value of `COOKIE_DATA` in the Config section of `import.py`; This value will be long, up to 5000 characters

   - In the payload of the request, copy the value in the `category/id` node and paste this into the value of `UNCATEGORIZED_CATEGORY_ID` in the Config section of `import.py`; This value will be in the format of `XXXXXXXX_XX`; *Note: Feel free to use a different category for your imported transactions*

## Limitations

- When manually adding transactions to Mint.com -- as well as via this app -- they are not attached to a specific bank account. This is a limitation of Mint.

- As explained above, all transactions are created in the "Uncategorized" category (or whatever category you chose when creating the sample transaction above). It is possible to import different categories per transaction, but would require much more code to download all your category IDs, and map them to your transactions.

- As stated above, this works with Mint.com as of mid-2022. If Mint is later updated, this may break until it is updated.