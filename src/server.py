from flask import Flask, jsonify

from OutlierFinder.outlierFinder import start_IF, start_LOF
from pymongo import MongoClient 
import datetime
 
server = Flask(__name__)

@server.route("/calculate-outlier/all", methods = ['GET'])
def outlier_all():
    try:
        myclient = MongoClient("mongodb://root:root@localhost:27017/") 

        db = myclient["robocup"]
        
        # Created or Switched to collection
        protocolCollection = db["protocols"]
        matchCollection = db['matches']

        protocols = list(protocolCollection.find({}))
        for protocol in protocols:
            protocolMatches = list(matchCollection.find({'protocolID':str(protocol.get('_id'))}))
            outliers = start_LOF(protocolMatches)
            for ifMatchId in start_IF(protocolMatches):
                if ifMatchId not in outliers:
                    outliers.append(ifMatchId)
            protocolCollection.update_one({'_id':protocol.get('_id')}, {'$set': {'outlierDetector': {'lastRan': datetime.datetime.now(), 'outliers': outliers}}})
        return "Success", 200
    except:
        return "Failure", 500


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8081)
