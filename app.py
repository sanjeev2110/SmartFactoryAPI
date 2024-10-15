from platform import machine
from flask import Flask, jsonify, request

app = Flask(__name__)

machines = [
    {"id": 1, "name": "Injection moulding", "status": "Running", "temperature": 75},
    {"id": 2, "name": "Blow moulding", "status": "Stopped", "temperature": 60},
    {"id": 3, "name": "BM2", "status": "Idle", "temperature": 65}
]

# Validate incoming machine data
def validate_machine_data(data):
    if "id" not in data or not isinstance(data["id"], int):
        return False, "ID is required and must be an integer."
    if "name" not in data or not isinstance(data["name"], str):
        return False, "Name is required and must be a string."
    if "status" not in data or not isinstance(data["status"], str):
        return False, "Status is required and must be a string."
    if "temperature" not in data or not isinstance(data["temperature"], int):
        return False, "Temperature is required and must be an integer."
    return True, ""

# Endpoint: Home page (Welcome message)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Smart Factory API!"})

# Endpoint: Get all machines
@app.route('/machines', methods=['GET'])
def get_machines():
    return jsonify({"machines": machines})

# Endpoint: Add a new machine (POST request)
@app.route('/machines', methods=['POST'])
def add_machine():
    new_machine = request.get_json()
    machines.append(new_machine)
    return jsonify({"message": "Machine added!", "machines": machines}), 201

# Endpoint: Get a specific machine by ID (GET request)
@app.route('/machines/<int:machine_id>', methods=['GET'])
def get_machine(machine_id):
    print(f"Requested machine ID: {machine_id}")
    print(f"Current machines list: {machines}")
    
    machine = next((m for m in machines if m["id"] == machine_id), None)
    if machine:
        return jsonify(machine)
    else:
        print(f"Machine with ID {machine_id} not found")
        return jsonify({"error": "Machine not found"}), 404
    

# Endpoint: Update a machine's details (PUT request)
@app.route('/machines/<int:machine_id>', methods=['PUT'])
def update_machine(machine_id):
    machine = next((m for m in machines if m["id"] == machine_id), None)
    if machine:
        updated_data = request.get_json()
        machine.update(updated_data)
        return jsonify({"message": "Machine updated!", "machine": machine})
    else:
        return jsonify({"error": "Machine not found"}), 404

# Endpoint: Delete a machine by ID (DELETE request)
@app.route('/machines/<int:machine_id>', methods=['DELETE'])
def delete_machine(machine_id):
    global machines
    machine = next((m for m in machines if m["id"] == machine_id), None)
    if machine:
        machines = [m for m in machines if m["id"] != machine_id]
        return jsonify({"message": "Machine deleted!", "machines": machines})
    else:
        return jsonify({"error": "Machine not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
