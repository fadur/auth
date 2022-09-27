#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import boto3
from helpers import secret_hash

ClientId = os.environ.get("CLIENT_ID")


async def register_cognito_user(username, password):
    client = boto3.client("cognito-idp")
    print(username)
    print(password)
    response = client.sign_up(
        ClientId=ClientId,
        SecretHash=secret_hash(username),
        Username=username,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": username},
        ],
    )
    return response


async def confirm_cognito_user(username, code):
    client = boto3.client("cognito-idp")
    response = client.confirm_sign_up(
        ClientId=ClientId,
        SecretHash=secret_hash(username),
        Username=username,
        ConfirmationCode=code,
    )
    return response
