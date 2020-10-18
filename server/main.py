from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
import string
import random
import os
import yfinance as yf

#from google.cloud import datastore, storage
#datastore_client = datastore.Client()

app = Flask(__name__)

def randomStringDigits(stringLength=6):

    lettersAndDigits = string.ascii_letters + string.digits

    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def oauth_ncr():

    url = "http://ncrdev-dev.apigee.net/digitalbanking/oauth2/v1/token"

    payload = 'grant_type=client_credentials&scopes=accounts%3Aread%2Ctransactions%3Aread%2Ctransfers%3Awrite%2Caccount%3Awrite%2Cinstitution-users%3Aread%2Crecipients%3Aread%2Crecipients%3Awrite%2Crecipients%3Adelete%2Cdisclosures%3Aread%2Cdisclosures%3Awrite'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic alI3RWg3dUF5cFQ0dEpMb0xVMmRBTVlHQ1l5ejZsVjg6T3FRZXQ0OE5YWDdTQXB4SA==',
      'transactionId': '77fd8baf-0903-4698-9139-bcea9b9214cb',
      'institutionId': '00516',
      'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload).json()

    return response.get("access_token") #access_token

def get_all_accs(auth):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-accounts/v1/accounts?hostUserId=HACKATHONUSER208"

    payload = {}
    headers = {
      'Authorization': 'Bearer {}'.format(auth),
      'transactionId': '03a7922d-aef8-4049-be97-9b0053e7ba6d',
      'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data = payload).json()

    return response

def make_transaction(auth, fromAccountHolderId, fromAccountId, toAccountId):

    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-transfers/v1/transfers?hostUserId=HACKATHONUSER208"

    payload = "{\n\t\"fromAccountHolderId\":\"15dc414ba1b6450280405c307a791b27\",\n\t\"fromAccountId\":\"rf5ao6Qclwsth9OfOvUb-EeV1m2BfmTzUEALGLQ3ehU\",\n\t\"toAccountId\":\"W4vrnyCIYqtzYybyi1dChNBtVD7kWbvrTEljsZq5z6Y\",\n\t\"amount\":{\n\t\t\"amount\":500.0\n\t}\n}"
    headers = {
      'Authorization': 'Bearer {}'.format(auth),
      'transactionId': 'a07e3cf7-9d68-4fdd-8a39-6c319fa88401',
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))

@app.route('/')
def root():
    #token = oauth_ncr()
    #accs = get_all_accs(token)
    #print(accs)
    return render_template("dashboard.html")
    #jsonify({"status":"200"})

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
