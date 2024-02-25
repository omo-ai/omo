import os
import json
import pytest
import requests

class TestUser:

    api_host = os.environ.get('API_HOST')

    register_endpoint = f"{api_host}/v1/auth/user/register"

    def test_register_user_email_only(self):
        payload = {'email': 'chris.han@blackarrow.software'}
        response = requests.post(self.register_endpoint, json.dumps(payload))
        assert response.status_code == 200

