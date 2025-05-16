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


def fetch_case_by_number(case_number):
    """Fetch the case using the case number"""
    try:
        query = f"SELECT Id, CaseNumber, Subject, Status, Priority FROM Case WHERE CaseNumber = '{case_number}'"
        result = sf.query(query)
        if result['totalSize'] == 0:
            return {'error': 'No case found with the provided case number'}
        return result['records'][0]
        # case=sf.Case.get(case_number)
        # return case
    except Exception as e:
        return {'error': 'Failed to fetch the case', 'details': str(e)}

@app.route('/find_case_by_number/<case_number>', methods=['GET'])
def fetch_case_by_number_route(case_number):
    result = fetch_case_by_number(case_number)
    return jsonify(result)

@app.route('/find_case_by_no', methods=['POST'])
def fetch_case_number_route():
    data = request.get_json()
    if not data or 'case_number' not in data:
        return jsonify({'error': 'Missing case_number in request'})

    case_number = data['case_number']
    result = fetch_case_by_number(case_number)
    return jsonify(result)

def update_case(case_id, update_data):
    """Update a case with given data"""
    try:
        result = sf.Case.update(case_id, update_data)
        return {'message': 'Case updated successfully', 'result': result}
    except Exception as e:
        return {'error': 'Failed to update the case', 'details': str(e)}

@app.route('/update_case/<case_id>', methods=['PATCH'])
def update_case_route(case_id):
    update_data = request.json
    result = update_case(case_id, update_data)
    return jsonify(result)


def delete_case_by_number(case_number):
    try:
        query = f"SELECT Id FROM Case WHERE CaseNumber = '{case_number}'"
        result = sf.query(query)
        if result['totalSize'] == 0:
            return {'error': 'No case found with the provided case number'}, 404
        case_id = result['records'][0]['Id']
        sf.Case.delete(case_id)
        return {'message': f'Case {case_number} deleted successfully'}
    except Exception as e:
        return {'error': 'Failed to delete the case', 'details': str(e)}

@app.route('/delete_case/<case_number>', methods=['DELETE'])
def delete_case_route(case_number):
    result = delete_case_by_number(case_number)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

def create_lead(lead_data):
    try:
        new_lead=sf.Lead.create(lead_data)
        return json.dumps(new_lead,indent=2)
    except Exception as e:
        error_message={'error':'failed to create the lead','details':str(e)}
        return error_message
@app.route('/create_lead',methods=['POST'])
def create_lead_route():
    lead_data=request.json
    result=create_lead(lead_data)
    return jsonify(result)

def fetch_lead_by_name(lead_name):
    try:
        query = f"SELECT Id, Name, Company, Email FROM Lead WHERE Name = '{lead_name}'"
        result = sf.query(query)
        if result['totalSize'] == 0:
            return {'error': 'No lead found with the provided lead name'}
        return result['records'][0]
    except Exception as e:
        return {'error': 'Failed to fetch the lead', 'details': str(e)}
@app.route('/find_lead_by_name/<lead_name>', methods=['GET'])
def fetch_lead_by_name_route(lead_name):
    result = fetch_lead_by_name(lead_name)
    return jsonify(result)
    
def update_lead(lead_name,update_data):
    try:
        query = f"SELECT Id FROM Lead WHERE Name = '{lead_name}'"
        result = sf.query(query)
        if result['totalSize'] == 0:
            return {'error': 'No lead found with the provided lead name'}
        lead_id = result['records'][0]['Id']
        sf.Lead.update(lead_id, update_data)
        return {'message': 'Lead updated successfully'}
    except Exception as e:
        return {'error': 'Failed to update the lead', 'details': str(e)}
@app.route('/update_lead/<lead_name>', methods=['PATCH'])
def update_lead_route(lead_name):
    update_data = request.json
    result = update_lead(lead_name, update_data)
    return jsonify(result)
    
def delete_lead_by_name(lead_name):
    try:
        query = f"SELECT Id FROM Lead WHERE Name = '{lead_name}'"
        result = sf.query(query)
        if result['totalSize'] == 0:
            return {'error': 'No lead found with the provided lead name'}, 404
        lead_id = result['records'][0]['Id']
        sf.Lead.delete(lead_id)
        return {'message': f'Lead {lead_name} deleted successfully'}
    except Exception as e:
        return {'error': 'Failed to delete the lead', 'details': str(e)}
@app.route('/delete_lead/<lead_name>', methods=['DELETE'])
def delete_lead_route(lead_name):
    result = delete_lead_by_name(lead_name)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
