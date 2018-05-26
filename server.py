#script um server requests zu handlen


from flask import Flask, jsonify, request
import requests
import urllib, json

app=Flask(__name__)

@app.route("/api")
def main():
    return jsonify({"new_scratch":[(1,2),(3,6),(3,7)]})



if __name__=="__main__":
    app.run(host='0.0.0.0')