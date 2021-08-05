''' Anand Koirala email: anand.koirala@cqumail.com
code for the video explained in https://www.youtube.com/watch?v=A61Zn026Ruw&t=110s '''
from flask import Flask, Response
from gevent.pywsgi import WSGIServer
import cv2
app = Flask(__name__)
video = cv2.VideoCapture(0)
@app.route('/')
def index():
    return "Default Message"
def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        #yield (b'--frame\r\n'
               #b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n'
               b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
               b'\r\n' + frame + b'\r\n')
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, threaded=True) #### this is developer environment and process one request at a time..
##production###  below is the way to stream in production so multiple requests gets accepted. pip3 install gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
