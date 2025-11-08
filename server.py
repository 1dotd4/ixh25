from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json
from game import Race

race = Race(n_servers=5)

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'

socketio = SocketIO(app)

# Dictionary to store users and their assigned rooms
users = {}

@app.route('/')
def index():
    return render_template('index.html')

# Handle new user joining
@socketio.on('join')
def handle_join(username):
    users[request.sid] = username  # Store username by session ID
    join_room(username)  # Each user gets their own "room"
    resdata = { 'username': username,
                'message': 'joined the chain'}
    emit("message", json.dumps(resdata), room=username)

# Handle user messages
@socketio.on('message')
def handle_message(message):
    username = users.get(request.sid, "Anonymous")  # Get the user's name
    data = json.loads(message)

    resdata = { 'username': username,
                'message': ''}
    
    if data['action'] == 'train':
        resdata = race.player_train(username)
        # resdata['message'] = "is training."
    elif data['action'] == 'buy':
        resdata = race.player_add(username)
        # resdata['message'] = "bought a car."
        # add_player(username)
    elif data['action'] == 'race':
        resdata = race.player_race(username)
        # resdata['message'] = "joined the race."
        
    emit("message", json.dumps(resdata), broadcast=True)  # Send to everyone

# Handle disconnects
@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, "Anonymous")
    resdata = { 'username': username,
                'message': 'left the chain'}
    emit("message", json.dumps(resdata), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
