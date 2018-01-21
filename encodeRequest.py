import os
import subprocess

#echo -n "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559" | openssl dgst -sha256 -hmac #"NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"

def encode(requestBody, secret):
    toEmit = "echo -n \"" + requestBody + "\" | openssl dgst -sha256 -hmac " + secret
    standardOut = str(subprocess.check_output(toEmit, shell=True))
    randomSubstring = standardOut[2:-3]
    return randomSubstring