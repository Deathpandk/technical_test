import sys
import os
import json
import asyncio
import websockets
import datetime
import firebase_admin
from firebase_admin import db
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from multiprocessing import Process

import pprint


async def send_msg(event, type_of, path, obj_id):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        msg = f"{type_of} {path} has been {event}, db_id:{obj_id}"
        await websocket.send(msg)


def get_time_from_path(type_of, path):
    try:
        time = getattr(os.path, f'get{type_of}time')(path)
        return datetime.datetime.utcfromtimestamp(time).strftime("%m/%d/%Y, %H:%M:%S")
    except:
        return ''


class Handler(FileSystemEventHandler):
    path = '.'
    ref = None
    def on_any_event(self, event):
        full_path = self.path + event.src_path[1:]
        data = {
            'name': event.src_path.split('\\')[-1],
            'is_file': os.path.isfile(full_path),
            'updated': get_time_from_path('m', full_path),
            'created': get_time_from_path('c', full_path),
            'path': full_path,
            'r_path': event.src_path,
            'event_type': event.event_type,
            'operation': event.__dict__,
        }

        obj = self.ref.push()
        obj.set(json.dumps(data))
        obj_id = obj._pathurl
        type_of = 'File' if data.get('is_file') else 'Directory'
        asyncio.run(send_msg(event.event_type, type_of, event.src_path, obj_id))


if __name__ == "__main__":

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(f'Initiating watchdog in {path}, end with ctrl + c')

    cred_obj = firebase_admin.credentials.Certificate('./python-interview-659bf-firebase-adminsdk-2d49b-d3f4242dbf.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':'https://python-interview-659bf-default-rtdb.firebaseio.com/'
        })

    ref = db.reference("/")

    event_handler = Handler()
    event_handler.path = os.getcwdb().decode('utf-8') if path == '.' else path
    event_handler.ref = ref

    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            observer.stop()





