from flask import Flask, render_template
from flask import request
from flask import make_response
import os
import json 
import requests
import hashlib

app = Flask(__name__)
@app.route('/')

def index():
    try:
        import googleclouddebugger
        googleclouddebugger.AttachDebugger()
    except ImportError:
        pass
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    print("in webhook")
    req = request.get_json(silent=True, force=True)
    print "webhook - print req: {}".format(req)
    intent = req['result']['metadata']['intentName']
    
    
    if intent == "accountType":
        print("webhook - intent is accountCheck.")
        type = req['result']['parameters']['type']
        output_obj = accountFollowup(type)
    else:
        output_obj = UnauthorizedRequest()

    res = json.dumps(output_obj, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    
    return r
def UnauthorizedRequest():
    return {
            "speech": "Transaction failed.",
            "displayText": "Transaction failed.", 
            }


def accountFollowup(type):
    print "in accountFollowup function."
    #try:
    
    return {
                "speech": "Reset password - Personal account or Business Account?",
                "displayText": "Reset password - Personal account or Business Account?",
                "contextOut": [{"name": "accountType", "lifespan": 10, "parameters": {"type":type}}],
                "source": ""
                        }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')