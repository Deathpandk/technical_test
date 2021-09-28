# Home assignment
## General description:
Monitor the files and folders changes inside a given path, store the metadata information of the changes in a firebase database and send a message to a guest with the information to retrieve the metadata from firebase. Then the guest will retrieve the information and store it.


## Detailed description
The main program will start monitoring files and folders in a given path, and once an event (rename:move/update:modify/creation/delete:remove) is registered, then
information about the change will be stored in firebase. The fields and data types to be stored are described below:

* collection(fields)
	- name:string / foldername or filename
	- is_file:int / 1 if is file or zero if is folder
	- updated:string utc-0 / if file exists or an empty string
	- created:string utc-0 / if file exists or an empty string
	- path:string / absolute path to the file or folder
	- r_path:string / relative path to the file or folder starting from the observed path
	- event_type:string
	- operation: "json string describing the operation, the fields used here are arbitrary"

Then the file monitor is going to send a message to a guest (who will be listening for messages). The message contains the information to retrieve the metadata from the registered event. Once the guest has the message, it will retrieve the event information from firebase and store it in a json file.

The communication between the monitor and guest is going to be using websockets, so the guest will have a websocket server, while the observer will have a websocket client.

So there is going to be a single program running all components. The program will be running and getting events until a ctrl+break or the terminal is closed.

The code will be reviewed in a git repository.


## Firebase connection settings
User email
test_user@mail.com

Password
111111

ProjectId
python-interview-659bf

Firebase account
firebase-adminsdk-2d49b@python-interview-659bf.iam.gserviceaccount.com

Project number
733554412993

Key_file / credentials certificate
python-interview-659bf-firebase-adminsdk-2d49b-d3f4242dbf.json

User UID
zbRaUmjDCVXKzZLubHbpEl1YcQv1

Web API Key
AIzaSyBklP1huC_c6aJTpWEWxZ6Du-Wqoz3k8gs

Realtime DB
https://python-interview-659bf-default-rtdb.firebaseio.com/

Note: the db is in test mode, so you can use it with certificate files (without username and password)
