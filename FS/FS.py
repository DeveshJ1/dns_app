
import json
import socket
import ipaddress
from flask import Flask, request, jsonify

app_fs = Flask(__name__)
#the fs-server was ran by terminal. I cd to the location of the fs folder
#then I ran docker build -t fs-server . (the dot is included)
# Then ran docker run --name fs-server -p 9090:9090 fs-server 
@app_fs.route('/register', methods=['PUT'])
def register_fs():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip') #ip address of docker container of fs
    ttl='10'
    TYPE='A'
    as_ip=data.get('as_ip')# ip address of docker container of as
    port=data.get('as_port')
    as_port=int(port)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Prepare DNS registration message
        dns_message = {
            'TYPE': TYPE,
            'NAME': hostname,
            'VALUE': ip, #ip address of docker container of fs
            'TTL': ttl
        }

        # Convert the message to bytes and send it to AS server
        sock.sendto(json.dumps(dns_message).encode(), (as_ip, as_port))
        response, _ = sock.recvfrom(1024)

        return jsonify({'message': response.decode()}), 201
    # Register with AS server via UDP


@app_fs.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')

    try:
        number = int(number)
        result = fibonacci(number)
        return jsonify({'result': result}), 200
    except ValueError:
        return jsonify({'error': 'Bad Format'}), 400

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == '__main__':
    app_fs.run(host='0.0.0.0', port=9090, debug=True)
