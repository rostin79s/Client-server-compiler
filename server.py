import json
from http.server import BaseHTTPRequestHandler, HTTPServer,HTTPStatus
import threading
import worker

class myHandler(BaseHTTPRequestHandler):
        count=0
        def do_POST(self):
                datalen = int(self.headers['Content-Length'])
                data = self.rfile.read(datalen)
                self.obj = json.loads(data)
                myHandler.count+=1
                name="client.json"
                f=open(name,"w")
                f.write(self.obj)
                f.close()
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(json.dumps(myHandler.count).encode())
                myHandler.p=threading.Thread(target=worker.mains)
                myHandler.p.start()
                
        def do_GET(self):
                request_path = self.path
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                if request_path[0:4]=="/job":
                        if myHandler.p.is_alive():
                                message = {
                                        "status":"your image is not ready"
                                }
                                self.wfile.write(json.dumps(message).encode())
                        else:
                                myHandler.url="/media/image{}.jpg".format(myHandler.count)
                                message={"download url":myHandler.url}
                                self.wfile.write(json.dumps(message).encode())
                elif request_path[0:6]=="/media":
                        with open('image.jpg', 'rb') as file: 
                                self.wfile.write(file.read())
                else:
                        self.wfile.write(json.dumps("bad request").encode())
                return

try:
        server = HTTPServer(('127.0.0.1', 1020), myHandler)
        print ('Started httpserver on port ' , 1001)
        
        server.serve_forever()

except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()
        
