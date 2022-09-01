#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import os

ClientId = os.environ.get('CLIENT_ID')


async def user_attributes(request):
    body = await request.json()
    name = body.get('name')
    phone_number = body.get('phone_number')
    access_token = request.headers.get('Authorization')
    print(access_token)
    client = boto3.client('cognito-idp')
    response = client.update_user_attributes(
        AccessToken=access_token.split(' ')[1],
        UserAttributes=[
            {
                'Name': 'name',
                'Value': name
            },
            {
                'Name': 'phone_number',
                'Value': phone_number
            },
        ],
    )
    return response
