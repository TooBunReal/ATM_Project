from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import *
import os
import json
from operator import itemgetter

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRESSQL_URI")
db.init_app(app)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@app.route('/api/insert_file', methods=['POST'])
def insert_file():
    files_json = request.get_json()
    if not isinstance(files_json, list):
        return json.dumps({"status": "Invalid payload format. Expected a list of files", "status_code": "400"})
    new_files = []
    status = []
    for file in files_json:
        try:
            new_file = Files(
                id=file.get('id'),
                title=file.get('id'),
                content=file.get('content')
            )
            new_files.append(new_file)
        except:
            status.append({"status": f"Bad Req {id}", "status_code": "400"})

    db.session.add_all(new_files)
    db.session.commit()
    status.append(
        {"status": "Files inserted successfully", "status_code": "200"})
    return json.dumps(status)


@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    files_json = request.get_json()
    status = []
    if not isinstance(files_json, list):
        return json.dumps({"status": "Invalid payload format. Expected a list of files", "status_code": "400"})
    for file_ids in files_json:
        try:
            get_id = file_ids.get('id')
            file_query = Files.query.get(get_id)
            print(file_query)
            if (file_query == None):
                raise Exception
            else:
                Files.query.filter_by(id=get_id).delete()
                status.append(
                    {"status": f"File ID {get_id} deleted successfully", "status_code": "200"})
        except:
            status.append(
                {"status": f"File ID {get_id} not found", "status_code": "404"})

        db.session.commit()

    return status


@app.route('/api/read_file', methods=['GET'])
def read_file():
    files = Files.query.all()
    file_list = [file.__dict__ for file in files]
    for file in file_list:
        file.pop('_sa_instance_state')
    return json.dumps(file_list, default=str)


@app.route('/api/allFile', methods=['GET'])
def get_all_file():
    files = Files.query.all()
    file_list = [file.__dict__ for file in files]
    for file in file_list:
        file.pop('_sa_instance_state')
    return json.dumps(file_list, default=str)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
