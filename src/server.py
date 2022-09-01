#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiohttp import web

from register import register_cognito_user, confirm_cognito_user
from auth import login, refresh_token, authorize
from user_attributes import user_attributes


async def index(request):
    username = request.query.get("username")
    password = request.query.get("password")
    response = await register_cognito_user(username, password)
    return web.json_response(response)


async def confirm(request):
    username = request.query.get("username")
    code = request.query.get("code")
    response = await confirm_cognito_user(username, code)
    return web.json_response(response)


async def sign_in(request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")
    response = await login(username, password)
    return web.json_response(response)


async def refresh(request):
    username = request.query.get("username")
    token = request.query.get("refresh_token")
    print(token)
    response = await refresh_token(username, token)
    return web.json_response(response)


async def auth(request):
    token = request.query.get("access_token")
    response, status = await authorize(token)
    return web.json_response(response, status=status)


async def user(request):
    response = await user_attributes(request)
    return web.json_response(response)


app = web.Application()
app.router.add_route("GET", "/", index)
app.router.add_route("GET", "/confirm", confirm)
app.router.add_route("POST", "/login", sign_in)
app.router.add_route("GET", "/refresh", refresh)
app.router.add_route("GET", "/auth", auth)
app.router.add_route("POST", "/user", user)
web.run_app(app)
