
from flask import Flask, request, jsonify
import json
import requests
import socket
app_us = Flask(__name__)
#the us-server was ran by terminal. I cd to the location of the us folder
#then I ran docker build -t us-server . (the dot is included)
#then ran docker run --name us-server -p 8080:8080 us-server

#this worked perfectly and yielded the correct output
#the url used for the whole application is: 
#http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=172.17.0.3&as_port=53533
#the fsport is 9090 as by direction and as port is 53533 is also by direction of lab 
#the as_ip is the ip address of the docker container which the as-server is running on

@app_us.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')#ip of the docker container of the AS file
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({'error': 'Bad Request'}), 400 
    body={
        'hostname':hostname,
        'ip': "172.17.0.2",#ip address of docker container of fs server
        #above is the one of the 2 parts that is hardcoded since I wasn't made clear of if
        #the put request for /register for the hostname is done through 
        #this user server or if a curl put method is used to register
        #the host name. It  has to be hardcoded if done through here
        #so it is hard coded it should be to the ip address of the docker container
        #of the fibonacci server. If running opn different ip adress of docker container of
        #fs file must be changed to that IP address. if curl request used however we can
        #remove this body and the put request made below
        'as_ip': as_ip,#ip adress of docker container of as
        'as_port':as_port
    }
     #must remove body assignment above too if curl used or comment out
        #if curl used for /register it should be of this format
        #curl -X PUT -H "Content-Type: application/json" -d '{"hostname": "fibonacci.com", "ip": "172.17.0.2", "as_ip": "172.17.0.3", "as_port": "53533"}' http://localhost:9090/register
        #where ip should ip adress of docker container of fs file and as_io is the ip adress of
        #the docker container containing as file.
    #if curl used as mentioned above for the put request for /register
    # we can remove or comment out the 3 lines below FROM HERE:
    header = {'Content-Type': 'application/json'}
    fs_url_put = f"http://172.17.0.2:{fs_port}/register"
    #above is the second hardcoded part again containg 
    #ip address of docker container of fs file so needs to be changed if it is different 
    #or if curl used must remove or comment out from body= to request.put line below
    #
    requests.put(fs_url_put, json=body, headers=header)
    #:TO HERE
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_us:
        query={
        'TYPE': 'A',
        'NAME': hostname
        }

        sock_us.sendto(json.dumps(query).encode(), (as_ip, int(as_port)))
        response, _ = sock_us.recvfrom(1024)
        json_object=json.loads(response.decode())
        fs_url = f"http://{json_object['VALUE']}:{fs_port}/fibonacci?number={number}"
        response = requests.get(fs_url) 
        return response.content, response.status_code


if __name__ == '__main__':
    app_us.run(host='0.0.0.0', port=8080, debug=True)
