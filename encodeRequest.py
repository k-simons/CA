import subprocess
import sys
import json
import os

# returns (apiKey, signature)
# requestBody should look like "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559"
def generateApiKeyAndSignature(requestBody, filePath):
    datastore = {}
    with open(filePath, 'r') as f:
        datastore = json.load(f)
    signature = encode(requestBody, datastore["secret"])
    apiKey = datastore["api-key"]
    return (apiKey, signature)

def encode(requestBody, secret):
    toEmit = "echo \"" + requestBody + "\\c\" | openssl dgst -sha256 -hmac \"" + secret + "\""
    standardOut = str(subprocess.check_output(toEmit, shell=True))
    randomSubstring = standardOut[2:-3]
    return randomSubstring
