import time
import json
import pprint
import asyncio
import websockets
import firebase_admin
from firebase_admin import db


cred_obj = firebase_admin.credentials.Certificate('./python-interview-659bf-firebase-adminsdk-2d49b-d3f4242dbf.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://python-interview-659bf-default-rtdb.firebaseio.com/'
})



async def listen_msgs(websocket, path):
    msg = await websocket.recv()
    print(msg)
    obj_id = msg.split('db_id:')[-1]
    while True:
        ref = db.reference(obj_id)
        data = ref.get()
        if data is None:
            time.sleep(0.5)
        else:
            break
    pprint.pprint(data)

    try:
        f = open("db_data.json", "r")
        file_data = json.loads(f.read())
    except (FileNotFoundError, json.JSONDecodeError):
        file_data = {}
    file_data[obj_id] = data
    f = open("db_data.json", "w")
    f.write(json.dumps(file_data))


async def main():
    async with websockets.serve(listen_msgs, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())