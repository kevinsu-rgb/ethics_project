from flask import Flask
from flask import render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
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

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)