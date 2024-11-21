from flask import Flask, request, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS
from bson.binary import Binary

#bones is password
uri = "mongodb+srv://admin:bones@ethicsproject.t0lhm.mongodb.net/?retryWrites=true&w=majority&appName=EthicsProject"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

database = client["ArtDataset"]
fs = GridFS(database)
file_metadata = database.file_meta

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('base.html')

@app.route('/upload')
def upload():
    with open("bmo.png", 'rb') as file:
        file_data = file.read()
    fs.put(file_data, artist = "john", artwork_name = "bmo")
    
    return 'Image has been uploaded!'

@app.route('/download')
def download():
    file_data = database.fs.files.find_one({"artist" : "john", "artwork_name" : "bmo"})
    
    with open("bmo2.png", 'wb') as file:
        file.write(fs.get(file_data['_id']).read())
        
    return 'finished downloading'

if __name__ == '__main__':
    app.run(debug=True)