import os

def remove_os_env_temporarily() -> dict:
    old_env = os.environ.copy()
    os.environ.clear()
    for key, value in old_env.items():
        if key.startswith("BOLT_PYTHON_"):
            os.environ[key] = value
    return old_env


def restore_os_env(old_env: dict) -> None:
    os.environ.update(old_env)


def get_mock_server_mode() -> str:
    """Returns a str representing the mode.

    :return: threading/multiprocessing
    """
    mode = os.environ.get("BOLT_PYTHON_MOCK_SERVER_MODE")
    if mode is None:
        # We used to use "multiprocessing"" for macOS until Big Sur 11.1
        # Since 11.1, the "multiprocessing" mode started failing a lot...
        # Therefore, we switched the default mode back to "threading".
        return "threading"
    else:
        return mode

valid_message_body = {
    "token": "abc123",
    "team_id": "TEAM_ID",
    "context_team_id": "TEAM_ID",
    "context_enterprise_id": None,
    "api_app_id": "API_APP_ID",
    "event": {
        "client_msg_id": "f7e40963-b186-4d32-b284-2d8a4b530e3e",
        "type": "message",
        "text": "Hello World",
        "user": "USER_ID",
        "ts": "1703165690.914109",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "OEqvo",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "Hello World"
                            }
                        ]
                    }
                ]
            }
        ],
        "team": "TEAM_ID",
        "channel": "CHANNEL_ID",
        "event_ts": "1703165690.914109",
        "channel_type": "channel"
    },
    "type": "event_callback",
    "event_id": "Ev06B8QVF8KW",
    "event_time": 1703165690,
    "authorizations": [
        {
            "enterprise_id": None,
            "team_id": "TEAM_ID",
            "user_id": "USER_ID2",
            "is_bot": True,
            "is_enterprise_install": True
        }
    ],
    "is_ext_shared_channel": False,
    "event_context": "4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDY1TFBLMlkxSCIsImFpZCI6IkEwNjZWUThFUFY1IiwiY2lkIjoiQzA2N0hIMUJaTTMifQ"
}