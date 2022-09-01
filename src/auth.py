#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import boto3
from helpers import secret_hash

ClientId = os.environ.get("CLIENT_ID")


async def login(username, password):
    client = boto3.client("cognito-idp")
    response = client.initiate_auth(
        ClientId=ClientId,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
            "SECRET_HASH": secret_hash(username),
        },
    )
    return response


async def refresh_token(username, refresh_token):
    client = boto3.client("cognito-idp")
    response = client.initiate_auth(
        ClientId=ClientId,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
            "REFRESH_TOKEN": refresh_token,
            "SECRET_HASH": secret_hash(username),
        },
    )
    return response


async def authorize(access_token):
    client = boto3.client("cognito-idp")
    response = None
    try:
        response = client.get_user(AccessToken=access_token)
        status = 200
    except Exception as e:
        response = {"error": e.__str__().split(":")[1]}
        status = 401
    return response, status
