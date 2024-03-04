
import socket
import json
import threading

#the as-server was ran by terminal. I cd to the location of the as folder
#then I ran docker build -t as-server . (the dot is included)
# Then ran docker run --name as-server -p 53533:53533 as-server 

# Database to store DNS records (in-memory for simplicity)
dns_database = {}
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 53533))
def dns_registration_handler():
        while True:
            data, addr = udp_socket.recvfrom(1024)
            try:
                dns_message = json.loads(data.decode())
                if 'VALUE' in dns_message:
                    hostname = dns_message.get('NAME')
                    ip = dns_message.get('VALUE')
                    ttl = dns_message.get('TTL')
                    TYPE = dns_message.get('TYPE')
            # Store DNS record in the database
                    dns_database[hostname] = {'ip': ip, 'ttl': ttl, 'type': TYPE}
            # Respond to the FS.py UDP socket
                    response_data = {'message': 'Registered successfully'}
                    udp_socket.sendto(json.dumps(response_data).encode(), addr)
                else:
                    query_type= dns_message.get('TYPE')
                    query_name= dns_message.get('NAME')
                    if query_name in dns_database:
                        dns_record = dns_database[query_name]
                        response_data = {
                            'TYPE': dns_record['type'],
                            'NAME': query_name,
                            'VALUE': dns_record['ip'],
                            'TTL': dns_record['ttl']
                        }
                        udp_socket.sendto(json.dumps(response_data).encode(), addr)
                    else:
                        error_response = {'error': 'Record not found'}
                        udp_socket.sendto(json.dumps(error_response).encode(), addr)
            except json.JSONDecodeError:
                udp_socket.sendto("not working".encode(), addr)  # Ignore invalid JSON messages
if __name__ == '__main__':
    dns_registration_handler()