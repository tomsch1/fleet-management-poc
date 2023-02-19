import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Device model

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Device(name='{self.name}', type='{self.type}', location='{self.location}')"

# Create database and default devices if db does not exist yet
@app.before_first_request
def create_tables():
    if not os.path.exists('instance/data.db'): 
        db.create_all()

        # Create 2  devices
        device_one = Device(id=112, name='Cool foods', type='Fridge', location='Office') 
        device_two = Device(id=358, name='Hot drinks', type='Coffee', location='Desk')
        db.session.add(device_one)
        db.session.add(device_two)
        db.session.commit()


@app.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    result = []
    for device in devices:
        result.append({'id': device.id, 'name': device.name, 'type': device.type, 'location': device.location})
    return jsonify(result)


@app.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    device = Device.query.get(id)
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    return jsonify({'id': device.id, 'name': device.name, 'type': device.type, 'location': device.location})


@app.route('/devices', methods=['POST'])
def add_device():
    name = request.json['name']
    type = request.json['type']
    location = request.json['location']
    device = Device(name=name, type=type, location=location)
    db.session.add(device)
    db.session.commit()
    return jsonify({'id': device.id, 'name': device.name, 'type': device.type, 'location': device.location}), 201

@app.route('/devices/<int:id>', methods=['POST'])
def add_device_with_id(id):
    device_exists = Device.query.get(id)
    if device_exists:
        return jsonify({'error': 'Device already exists'}), 404
    name = request.json['name']
    type = request.json['type']
    location = request.json['location']
    device = Device(id=id, name=name, type=type, location=location)
    db.session.add(device)
    db.session.commit()
    return jsonify({'id': device.id, 'name': device.name, 'type': device.type, 'location': device.location}), 201

@app.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    device = Device.query.get(id)
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    device.name = request.json.get('name', device.name)
    device.type = request.json.get('type', device.type)
    device.location = request.json.get('location', device.location)
    db.session.commit()
    return jsonify({'id': device.id, 'name': device.name, 'type': device.type, 'location': device.location})


@app.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    device = Device.query.get(id)
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    db.session.delete(device)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')
