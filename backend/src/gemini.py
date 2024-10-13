import aiohttp
import asyncio
import typing_extensions as typing
import json
import pandas as pd
import time

# промт к gemini

promtt = ''
my_api = ['YOUR_API_KEY'] #нужен gemini apikey

#запрос к gemini через rest api
async def request_to_model(promt, api_id, model = 0):
    models = ['gemini-1.5-flash-latest','gemini-1.5-pro-latest']
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{models[model]}:generateContent'
    params = {'key': my_api[api_id]}
    headers = {'Content-Type': 'application/json'}
    # proxies = 'https://51.159.107.240/'
    json_data = {'contents': [{'parts': [{'text': promt}]}],'generationConfig': {'temperature': 0.5 },'safetySettings': [{'category': 'HARM_CATEGORY_DANGEROUS_CONTENT','threshold': 'BLOCK_NONE',},],}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, params=params, headers=headers, json=json_data) as response:
            return await response.json()

text = ""
def text_init():
    global text
    text = """"""
# n=5
text_init()
pre_text=f"\n{text}"
# tasks.append(asyncio.create_task())
