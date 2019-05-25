import pickle

def save_messages(messages):
    """Save messages so they don't have to be requested from GroupMe servers every time."""
    with open('messages.pkl', 'wb') as save_file:
        pickle.dump(messages, save_file)


def load_messages():
    """Load saved messages"""
    with open('messages.pkl', 'rb') as save_file:
        return pickle.load(save_file)