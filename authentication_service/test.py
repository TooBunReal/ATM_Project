import requests
import json

base_url = 'http://localhost:5000'

def wipe_database():
    wipe_url = f'{base_url}/wipe_database'
    response = requests.post(wipe_url)
    print(f'Wipe Database Request: {response.request.method} {response.request.url}')
    print(f'Request Headers: {response.request.headers}')
    print(f'Request Body: {response.request.body}')
    print(f'Response Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')
    print('')

def test_user_registration():
    url = f'{base_url}/register'
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(f'Registration Request: {response.request.method} {response.request.url}')
    print(f'Request Headers: {response.request.headers}')
    print(f'Request Body: {response.request.body}')
    print(f'Response Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')
    print('')

def test_user_login():
    url = f'{base_url}/login'
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(f'Login Request: {response.request.method} {response.request.url}')
    print(f'Request Headers: {response.request.headers}')
    print(f'Request Body: {response.request.body}')
    print(f'Response Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')
    print('')


def test_protected_resource_access():
    register_url = f'{base_url}/register'
    login_url = f'{base_url}/login'

    register_data = {'username': 'testuser', 'password': 'testpassword'}
    requests.post(register_url, headers={'Content-Type': 'application/json'}, data=json.dumps(register_data))

    login_data = {'username': 'testuser', 'password': 'testpassword'}
    login_response = requests.post(login_url, headers={'Content-Type': 'application/json'}, data=json.dumps(login_data))
    access_token = login_response.json().get('access_token')

    protected_url = f'{base_url}/protected'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(protected_url, headers=headers)

    print(f'Protected Resource Access Request: {response.request.method} {response.request.url}')
    print(f'Request Headers: {response.request.headers}')
    print(f'Response Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

if __name__ == '__main__':
    #wipe_database()
    test_user_registration()
    test_user_login()
    test_protected_resource_access()
