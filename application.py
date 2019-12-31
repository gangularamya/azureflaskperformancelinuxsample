from flask import Flask, g, make_response, request
from pyinstrument import Profiler
import random
import json

profiler = Profiler()
app = Flask(__name__)

@app.before_request
def before_request():
    if "profile" in request.args:
        g.profiler = Profiler()
        g.profiler.start()

@app.route("/")
def hello():
    return "Hello World!"
    
    
@app.route("/query")
def query():
    # below line is required while running app on azure
    f = open("/home/"+str(random.randint(1,1100))+".html","w+")
    # uncomment while running locally
    # f = open(str(random.randint(1,1100))+".html","w+")
    profiler.start()
    args = request.args.get('args')
    output = fibnonci_approach(int(args))
    profiler.stop()
    f.write(profiler.output_html())
    # print(profiler.output_text(unicode=True, color=True)) 
    return json.dumps(output)
     

@app.after_request
def after_request(response):
    if not hasattr(g, "profiler"):
        return response
    g.profiler.stop()
    output_html = g.profiler.output_html()
    return make_response(output_html)

def fibnonci_approach(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibnonci_approach(n - 1) + fibnonci_approach(n - 2)
     

if __name__ == "__main__":
    app.run() 
   