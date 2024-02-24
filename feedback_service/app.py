<<<<<<< HEAD
from flask import Flask, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
=======
from flask import Flask, request
>>>>>>> origin/fix-docker
from dotenv import load_dotenv
from models import *
import os
import json
<<<<<<< HEAD
from operator import itemgetter
=======
>>>>>>> origin/fix-docker

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRESSQL_URI")
db.init_app(app)
SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")


@app.route('/api/insert_feedback', methods=['POST'])
def insert_feedback():
    feedbacks_json = request.get_json()
    if not isinstance(feedbacks_json, list):
        return json.dumps({"status": "Invalid payload format. Expected a list of feedbacks", "status_code": "400"})
    new_feedbacks = []
    status = []
    for feedback in feedbacks_json:
        try:
            new_feedback = Feedbacks(
                name=feedback.get('name'),
                content=feedback.get('content')
            )
            new_feedbacks.append(new_feedback)
        except:
            status.append({"status": f"Bad Req {id}", "status_code": "400"})

    db.session.add_all(new_feedbacks)
    db.session.commit()
    status.append(
        {"status": "feedbacks inserted successfully", "status_code": "200"})
    return json.dumps(status)


<<<<<<< HEAD
# @app.route('/api/delete_feedback', methods=['POST'])
# def delete_feedback():
#     feedbacks_json = request.get_json()
#     status = []
#     if not isinstance(feedbacks_json, list):
#         return json.dumps({"status": "Invalid payload format. Expected a list of feedbacks", "status_code": "400"})
#     for feedback_ids in feedbacks_json:
#         try:
#             get_id = feedback_ids.get('id')
#             feedback_query = Feedbacks.query.get(get_id)
#             if (feedback_query == None):
#                 raise Exception
#             else:
#                 Feedbacks.query.filter_by(feedback_id=get_id).delete()
#                 status.append(
#                     {"status": f"feedback ID {get_id} deleted successfully", "status_code": "200"})
#         except:
#             status.append(
#                 {"status": f"feedback ID {get_id} not found", "status_code": "404"})

#         db.session.commit()

#     return status
=======
@app.route('/api/delete_feedback', methods=['POST'])
def delete_feedback():
    feedbacks_json = request.get_json()
    status = []
    if not isinstance(feedbacks_json, list):
        return json.dumps({"status": "Invalid payload format. Expected a list of feedbacks", "status_code": "400"})
    for feedback_ids in feedbacks_json:
        try:
            get_id = feedback_ids.get('id')
            feedback_query = Feedbacks.query.get(get_id)
            if (feedback_query == None):
                raise Exception
            else:
                Feedbacks.query.filter_by(feedback_id=get_id).delete()
                status.append(
                    {"status": f"feedback ID {get_id} deleted successfully", "status_code": "200"})
        except:
            status.append(
                {"status": f"feedback ID {get_id} not found", "status_code": "404"})

        db.session.commit()

    return status

>>>>>>> origin/fix-docker

@app.route('/api/allfeedback', methods=['GET'])
def get_all_feedback():
    feedbacks = Feedbacks.query.all()
<<<<<<< HEAD
    feedback_list  = [feedback.__dict__ for feedback in feedbacks]
    for feedback in feedback_list:
        feedback.pop('_sa_instance_state')
    return json.dumps(feedback_list,default=str)
=======
    feedback_list = [feedback.__dict__ for feedback in feedbacks]
    for feedback in feedback_list:
        feedback.pop('_sa_instance_state')
    return json.dumps(feedback_list, default=str)
>>>>>>> origin/fix-docker


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
