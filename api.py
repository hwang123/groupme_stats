import requests

def get_messages(group, token):
    """Gets all messages from a group since it was created. Requires that the token
    belongs to an account that is currently a member of the group. Paged 100 messages
    per request, so might take a while for groups with 1000+ messages."""

    GROUP_URI = 'https://api.groupme.com/v3/groups/' + str(group)
    messages = []
    message_id = get_latest_message(group, token)['id']

    while True:
        request_string = GROUP_URI + '/messages?token=' + token + '&before_id=' + str(message_id) + '&limit=' + '100'
        r = requests.get(request_string)
        try:
            messages += r.json()['response']['messages']
            message_id = messages[-1]['id']
        except ValueError:
            break
        print(len(messages))

    return messages


def get_latest_message(group, token):
    """Gets the most recent message from a group. Token must be valid for the group."""

    GROUP_URI = 'https://api.groupme.com/v3/groups/' + str(group)
    r = requests.get(GROUP_URI + '/messages?token=' + token + '&limit=1')
    return r.json()['response']['messages'][0]