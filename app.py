from flask import Flask, request, render_template, send_file
import io
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


@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')


@app.route('/download_page')
def download_page():
    return render_template('download.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['artwork_file']    
    artist_name = request.form['artist_name']
    artwork_name = request.form['artwork_name']
    file_data = file.read()
    fs.put(file_data, artist=artist_name, artwork_name=artwork_name)
    return render_template('confirmation.html')


@app.route('/download', methods=['POST'])
def download():
    artist = request.form['artist_name']
    artwork_name = request.form['artwork_name']
    file_data = database.fs.files.find_one({"artist": artist, "artwork_name": artwork_name})
    if file_data:
        file_id = file_data['_id']
        grid_out = fs.get(file_id)
        file_stream = io.BytesIO(grid_out.read())
        file_stream.seek(0)
        return send_file(file_stream, as_attachment=True, download_name=f"{artwork_name}-{artist}-download.png", mimetype='image/png')
    else:
        return "File not found", 404


if __name__ == '__main__':
    app.run(debug=True)