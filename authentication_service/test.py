import requests
import json

base_url = 'http://localhost:5000'

def test_user_registration():
    url = f'{base_url}/register'
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    print(response.json())

def test_user_login():
    url = f'{base_url}/login'
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    print(response.json())

def test_protected_resource_access():
    # Assuming you have registered and logged in a user in the previous tests
    register_url = f'{base_url}/register'
    login_url = f'{base_url}/login'

    # Register a test user
    register_data = {'username': 'testuser', 'password': 'testpassword'}
    requests.post(register_url, headers={'Content-Type': 'application/json'}, data=json.dumps(register_data))

    # Login to obtain an access token
    login_data = {'username': 'testuser', 'password': 'testpassword'}
    login_response = requests.post(login_url, headers={'Content-Type': 'application/json'}, data=json.dumps(login_data))
    access_token = login_response.json().get('access_token')

    # Access the protected resource using the obtained access token
    protected_url = f'{base_url}/protected'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(protected_url, headers=headers)

    print(response.status_code)
    print(response.json())

if __name__ == '__main__':
    test_user_registration()
    test_user_login()
    test_protected_resource_access()
