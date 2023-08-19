##########################################################################
############# Script para el envio de datos a FireBase ####################
##########################################################################

# Import database module.
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

fecha = datetime.today().strftime('%Y-%m-%d')
hora = datetime.today().strftime('%H:%M:%S')
# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')
# Initialize the app with a None auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {'databaseURL': 'https://grupo-6-43b09-default-rtdb.firebaseio.com/'})


def sendDataFireBase(cpu, ram, usoDisco):
    try:
        ref = db.reference('')
        posts_ref = ref.child('grupo6')
        new_post_ref = posts_ref.push()
        new_post_ref.set({
            'fecha': fecha,
            'hora': hora,
            'grupo6Datos': cpu,
            'grupo6Datos': ram,
            'grupo6Datos': usoDisco,
        })
        print("Registro guardado")
    except  Exception as e:
        print(e)

# sendDataFireBase()
# sendDataFireBase(200)