#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hmac
import hashlib
import base64

#ClientId = os.environ.get('CLIENT_ID')
ClientId = "1z2x3c4v5b6n7m81z2x3c4v5b6n7m8"

# client_secret = os.environ.get('CLIENT_SECRET')
client_secret = "1z2x3c4v5b6n7m8"


def secret_hash(username):
    msg = username + ClientId
    dig = hmac.new(
        str(client_secret).encode('utf-8'),
        msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
