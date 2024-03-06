kubectl create secret generic openai-api-key \
--from-literal=token='***REMOVED***' -n omo-api

kubectl create secret generic pinecone-api-key \
--from-literal=token='37a5136a-01b3-42d2-b90c-c448f66452eb' -n omo-api

kubectl create secret generic pinecone-index \
--from-literal=token='alloydigital-googledrive' -n omo-api

kubectl create secret generic pinecone-env \
--from-literal=env='gcp-starter' -n omo-api



docker compose --env-file omo_api/conf/envs/.env.komodo --env-file omo_api/conf/.env.development up

Slack attributes:

{'blocks': [{'block_id': 'i9snn',
             'elements': [{'elements': [{'text': 'What is Aperture?',
                                         'type': 'text'}],
                           'type': 'rich_text_section'}],
             'type': 'rich_text'}],
 'channel': 'CHANNEL_ID',
 'channel_type': 'channel',
 'client_msg_id': 'MSG_ID',
 'event_ts': '1702540537.014409',
 'team': 'TEAM_ID',
 'text': 'What is Aperture?',
 'ts': '1702540537.014409',
 'type': 'message',
 'user': 'USER_ID'}


         # Create temp registration

        # Check if the Slack User ID exists - they already installed
        # If doesn't exist - 
            # create the User # redirect to user registration page with slack context

        # Check if slack team worksapce ID exists
            # if not
            # create the team
            #   team_config with empty empty apps
        # if user and team does not exist (we have not seen them before)
            # put user in default project
            # create a pinecone index for the user
            # create an API key (manual) - default api key for user


DEBUG:    2023-12-22 04:37:20 Installation data missing for enterprise: none, team: TEAM_ID: [Errno 2] No such file or directory: '/root/.bolt-app-installation/6190801100051.6233824499991/none-TEAM_ID/installer-latest'
INFO:     172.16.1.83:13552 - "POST /api/v1/slack/message HTTP/1.1" 200 OK
DEBUG:    2023-12-22 04:37:20 Installation data missing for enterprise: none, team: TEAM_ID: [Errno 2] No such file or directory: '/root/.bolt-app-installation/6190801100051.6233824499991/none-TEAM_ID/bot-latest'
DEBUG:    2023-12-22 04:37:20 No installation data found for enterprise_id: None team_id: TEAM_ID
ERROR:    2023-12-22 04:37:20 Although the app should be installed into this workspace, the AuthorizeResult (returned value from authorize) for it was not found.
INFO:     2023-12-22 04:37:20 b'{"token":"abc123","team_id":"TEAM_ID","context_team_id":"TEAM_ID","context_enterprise_id":null,"api_app_id":"API_APP_ID","event":{"client_msg_id":"c5f6d147-72a3-4a13-98a9-9f9821582120","type":"message","text":"hello","user":"USER_ID","ts":"1703219840.100169","blocks":[{"type":"rich_text","block_id":"ZL1yL","elements":[{"type":"rich_text_section","elements":[{"type":"text","text":"hello"}]}]}],"team":"TEAM_ID","channel":"D067NVADT41","event_ts":"1703219840.100169","channel_type":"im"},"type":"event_callback","event_id":"Ev06BCKQND4L","event_time":1703219840,"authorizations":[{"enterprise_id":null,"team_id":"TEAM_ID","user_id":"USER_ID","is_bot":false,"is_enterprise_install":false}],"is_ext_shared_channel":false,"event_context":"4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDY1TFBLMlkxSCIsImFpZCI6IkEwNjZWUThFUFY1IiwiY2lkIjoiRDA2N05WQURUNDEifQ"}'
INFO:     2023-12-22 04:37:20 b':warning: We apologize, but for some unknown reason, your installation with this app is no longer available. Please reinstall this app into your workspace :bow:'


https://github.com/slackapi/bolt-python/issues/134
https://github.com/slackapi/bolt-python/issues/664
https://github.com/slackapi/bolt-python/issues/723#issuecomment-1256366868

e8134017fe7347cab66e1ed50777f8ac


export NOTION_API_KEY='secret_X8ieA0y2zUBYjH7REOPmTByXEScAyvDsSG7JVMxsTvA' \
curl -X POST 'https://api.notion.com/v1/databases/Customer-Segment-422c1b460b4d47bf86757ec36106e229/query' \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H 'Notion-Version: 2022-06-28' \
  -H "Content-Type: application/json"

  curl -X POST 'https://api.notion.com/v1/search' \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2022-06-28' \
  --data '{
    "filter": {
        "value": "page",
        "property": "object"
    }
  }'

  curl -X POST http://localhost:8000/api/v1/web/answer/?question=hellowlrld


  # Release
  Added OPENAI_MODEL env var