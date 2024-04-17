from pymongo import MongoClient

# Create a client
client = MongoClient("localhost", 27017)

# Access the 'chatbot' database
db = client['chatbot']

# Access the 'sessions' collection
sessions = db['sessions']

# Store a chat session
def store_session(file_name, conversation):
    session = {
        'file_name': file_name,
        'conversation': conversation
    }
    sessions.update_one(
        {'file_name': file_name},  # query
        {'$set': session},  # new data
        upsert=True  # create a new document if no document matches the query
    )

# Retrieve a chat session
def get_session(file_name):
    session = sessions.find_one({'file_name': file_name})
    return session['conversation'] if session else None

def get_all_sessions():
    return [session['file_name'] for session in sessions.find()]