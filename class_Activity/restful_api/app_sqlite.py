from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Client {self.name}>'

    def to_dict(self):
        """Utility method to serialize the object into a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


@app.route('/create-db')
def create_db():
    db.create_all()
    return "Database tables created!"

@app.route('/')
def index():
    return "Hello, Flask is running!"

#Create a New Client (POST)
@app.route('/api/clients', methods=['POST'])
def add_client():
    data = request.get_json()
    new_client = Client(name=data['name'], email=data['email'])
    db.session.add(new_client)
    db.session.commit()
    return jsonify(new_client.to_dict()), 201

#Get All Clients (GET)
@app.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients])

#Get a Specific Client by ID (GET)
#http://127.0.0.1:5000/api/clients/1
@app.route('/api/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client.to_dict())

# Update a Client (PUT)
@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    db.session.commit()
    return jsonify(client.to_dict())

# Delete a Client (DELETE)
@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted successfully."})



if __name__ == '__main__':
    # Run the app on localhost with debugging enabled
    app.run(debug=True)