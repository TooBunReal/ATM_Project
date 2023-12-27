import jwt
import requests
from service import SERVICES


def manage_operation(operation, file_endpoint, request_json):
    # auth_response = requests.post(
    #     SERVICES['authentication'], json=request_json)
    # if auth_response.status_code == 200:
    #     token_response = auth_response.json()
    #     token = token_response.get('token')

    #     roles = decode_token(token).get('role', '')

    #     if roles == 'admin' or (roles == 'user' and operation == 'read'):
    # Gọi dịch vụ Management với token và thực hiện operation
    management_response = requests.post(
        SERVICES['file_service'] + '/' + file_endpoint,
        json={'token': token, 'operation': operation, 'files': request_json}).text
    return {'status': 'success', f'management_{operation}_response': management_response}
    #     else:
    #         return {'status': 'error', 'error': 'Unauthorized'}
    # else:
    #     return {'status': 'error', 'error': 'Authentication failed'}


# def file_operation_get(operation, file_endpoint, request_json):
#     requests.get(
#         SERVICES['file_service'] + '/' + file_endpoint,
#         json={'token': token, 'operation': operation, 'files': request_json}).text


def decode_token(token):
    return jwt.decode(token, verify=False)
