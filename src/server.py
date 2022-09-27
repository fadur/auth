#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from aiohttp import web
import aiohttp_cors

from register import register_cognito_user, confirm_cognito_user
from auth import login, refresh_token, authorize
from user_attributes import user_attributes

logging.basicConfig(level=logging.DEBUG)


async def index(request):
    body = await request.json()
    password = body.get("password")
    email = body.get("email")
    username = email
    try:
        response = await register_cognito_user(username, password)
    except Exception as e:
        erro_msg = str(e)
        error = erro_msg.split(":")[1:]
        msg = "\n".join(error)
        response = {"error": msg}
        return web.json_response(response, status=500)
    return web.json_response(response)


async def confirm(request):
    body = await request.json()
    username = body.get("username")
    code = body.get("code")
    try:
        response = await confirm_cognito_user(username, code)
    except Exception as e:
        response = {"error": str(e)}
    return web.json_response(response)


async def sign_in(request):
    body = await request.json()
    username = body.get("username")
    if not username:
        username = body.get("email")
    password = body.get("password")
    try:
        response = await login(username, password)
    except Exception as e:
        erro_msg = str(e)
        error = erro_msg.split(":")[-1]
        response = {"error": error}
        return web.json_response(response, status=500)
    return web.json_response(response)


async def refresh(request):
    body = await request.json()
    token = body.get("token")
    username = body.get("username")

    if not username:
        username = body.get("email")

    try:
        response = await refresh_token(username, token)
    except Exception as e:
        response = {"error": str(e)}
        return web.json_response(response, status=500)
    return web.json_response(response)


async def auth(request):
    token = request.query.get("access_token")
    response, status = await authorize(token)
    return web.json_response(response, status=status)


async def user(request):
    response = await user_attributes(request)
    return web.json_response(response)


app = web.Application()
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    },
)

# secure cookie session
# session_middleware = aiohttp_session.cookie_storage.EncryptedCookieStorage(
#     secret_key=os.urandom(32)
#


cors.add(app.router.add_post("/register", index))
cors.add(app.router.add_post("/confirm", confirm))

app.router.add_route("POST", "/login", sign_in)
app.router.add_route("POST", "/refresh", refresh)
app.router.add_route("GET", "/auth", auth)
app.router.add_route("POST", "/update-profile", user)
web.run_app(app)
