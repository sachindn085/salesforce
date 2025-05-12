from flask import Flask, request, jsonify
from simple_salesforce import Salesforce
import os
import json
from dotenv import load_dotenv
load_dotenv()


app=Flask(__name__)
sf = Salesforce(
    username=os.getenv("SF_USERNAME"),
    password=os.getenv("SF_PASSWORD"),
    security_token=os.getenv("SF_SECURITY_TOKEN")
)
def create_case(case_data):
    """create new case based on new data"""
    try:
        new_case=sf.Case.create(case_data)
        return json.dumps(new_case,indent=2)
    except Exception as e:
        error_message={'error':'failed to create the case','details':str(e)}
        return error_message
    
@app.route('/create_case',methods=['POST'])
def create_case_route():
    case_data=request.json
    result=create_case(case_data)
    return jsonify(result)

def fetch_case(case_id):
    """fetch the case using the case_id"""
    try:
        case=sf.Case.get(case_id)
        return case
    except Exception as e:
        error_message={'error':'failed to fetch the case','details':str(e)}
        return error_message
    
@app.route('/find_case/<case_id>',methods=['GET'])
def fetch_case_route(case_id):
    result=fetch_case(case_id)
    return jsonify(result)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
