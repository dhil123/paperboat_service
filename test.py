# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

  
# creating a Flask app
app = Flask(__name__)
  
# on the terminal 'type': curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world jhjh"
        return jsonify({'data': data})
  
  
# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal 'type': curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/sqr/<int:num>', methods = ['GET'])
def disp(num):
  
    return jsonify({'data': num**2})

@app.route('/getwatchlist', methods = ['GET'])
@cross_origin()
def getwatchlist():
  
    return jsonify({'items': [
        {'id':1, 'symbol' : 'RIL', 'ltp':2501.5, 'change':1.5, 'type':'equity'},
        {'id':2, 'symbol' : 'NIFTY', 'ltp':17000, 'change':-0.5, 'type':'index'},
        {'id':3, 'symbol' : 'BANKNIFTY', 'ltp':35000, 'change':-0.5, 'type':'index'},
        {'id':4, 'symbol' : 'SAIL', 'ltp':120, 'change':-0.5, 'type':'equity'}
    ]})
  
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)