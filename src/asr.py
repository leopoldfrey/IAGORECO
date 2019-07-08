from __future__ import print_function
import bottle, osc, sys

class ASR:
    global is_restart_needed

    def __init__(self, osc_server_port=9000, osc_client_host='127.0.0.1', osc_client_port=9001, http_server_port=8080):
        self.osc_server_port = osc_server_port
        self.osc_client_host = osc_client_host
        self.osc_client_port = osc_client_port
        osc.setup(osc_client_host, osc_client_port)

        self.http_server_port = http_server_port
        self.silent = True
        self.sentence_num = 0
        self.is_restart_needed = True
        
        self.http_server = bottle.Bottle()

        self.silent = False
        self.osc_server = osc.Server(host='0.0.0.0', port=self.osc_server_port, callback=self.osc_server_message)
        self.osc_server.run(non_blocking=True)

        print()
        print('*** Please open chrome at http://127.0.0.1:%d' % self.http_server_port)
        print()

        self.http_server.get('/', callback=self.index)
        self.http_server.post('/result', callback=self.result)
        self.http_server.get('/need_restart', callback=self.need_restart)
        self.http_server.run(host='localhost', port=self.http_server_port, quiet=True)

    def osc_server_message(self, message):
        # print('OSC message = "%s"' % message)
        if message == '/record':
            self.silent = False
        elif message == '/pause':
            self.silent = True
        elif message == '/restart':
            # self.osc_server.shutdown()
            # os.execlp(sys.executable, sys.executable, *sys.argv)
            self.is_restart_needed = True
            self.silent = False
        elif message == '/exit':
            self.osc_server.shutdown()
            self.http_server.close()
            sys.exit(0)

    def result(self):
        result = {'transcript': bottle.request.forms.getunicode('transcript'),
                'confidence': float(bottle.request.forms.get('confidence', 0)),
                'sentence': int(bottle.request.forms.sentence)}
        mess = ("   " + result['transcript'] + "   ").encode('utf-8').strip('<eos>')
        if self.silent == True:
            if result['sentence'] == 1:
                print("(pause)phrase  _" + mess)
                self.sentence_num += 1
            else:
                print("(pause)mots    _" + mess)
            return 'ok'
        if result['sentence'] == 1:
            print("phrase  _" + mess)
            osc.client.send_sentence(self.sentence_num, mess)
            self.sentence_num += 1
        else:
            print("mots    _" + mess)
            osc.client.send_words(self.sentence_num, mess)
        return 'ok'

    def need_restart(self):
        if self.is_restart_needed:
            self.is_restart_needed = False
            return 'yes'
        return 'no'
   
    def index(self):
        return '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf8">
        <script src="https://code.jquery.com/jquery-2.2.4.min.js"></script> 
        <style>
body
{
font-family:helvetica;
}
p
{
padding:0;
margin:0;
font-size:12px;
line-height:1;
}
        </style>
        <title>ASR Bridge</title>
    </head>
    <body>
        <!--h3>ASR Bridge</h3-->
        <script>
var recognition = new webkitSpeechRecognition();
if(recognition == null) {
    $('body').append('<p><b>!!! ASR Bridge ERROR: webkitSpeechRecognition not available !!!</b></p>');
} else {
    $('body').append('<p><b>--- ASR Bridge Ready --- </b></p>');
}
recognition.continuous = true;
recognition.interimResults = true;
recognition.maxAlternatives = 1;
//recognition.lang = "fr-FR";
recognition.lang = "en-US";
recognition.onresult = detect;
recognition.onend = function(event) { recognition.start(); console.log('event: end'); }
recognition.onstart = function(event) { console.log('event: start'); }
recognition.start();

var timer = null;
var p = $('<p></p>');
$('body').append(p);
function detect(event) {
    if(timer != null) {
        clearTimeout(timer);
    }
    for (var i = event.resultIndex; i < event.results.length; i++) {
        console.log(event.results[i]);
        if(event.results[i][0].confidence < .5) continue;
        $(p).text(event.results[i][0].transcript);
        if(event.results[i].isFinal) {
            p = $('<p></p>');
            $('body').append(p);
        }
        $.post('/result', {transcript: String(event.results[i][0].transcript), 
                confidence: event.results[i][0].confidence, 
                sentence: event.results[i].isFinal ? 1 : 0
                });
        timer = setTimeout(function() {
            recognition.stop();
            timer = null;
        }, 5000);
    }
}

setInterval(function() {
   $.get('/need_restart', function(data) {
   	   if(data == 'yes') {
       		console.log('/need_restart');
       		window.location.reload(false);
       }
   })
}, 100);

        </script>
    </body>
</html>
'''


if __name__ == '__main__':
    if len(sys.argv) == 1:
        ASR();
    elif len(sys.argv) == 5:
        ASR(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port> <http-server-port>')
