from flask import Flask,requert,render_template
import urllib
import json

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("form.html")

@app.route('/aml', methods=['GET','POST'])
def aml():
    # request.values['p1']

    data = {
        "Inputs": {
            "WebServiceInput0":
            [
                {
                    'Pregnancies': request.values['p1'],
                    'Glucose': "request.values['p2'],
                    'BloodPressure': request.values['p3'],
                    'SkinThickness': request.values['p4'],
                    'Insulin': request.values['p5'],
                    'BMI': request.values['p6'],
                    'DiabetesPedigreeFunction': request.values['p7'],
                    'Age': request.values['p8'],
                    'Outcome': "1",
                },
            ],
        },
        "GlobalParameters": {
        }
    }
    
    body = str.encode(json.dumps(data))
    
    url = 'http://104.215.27.140:80/api/v1/service/model3729/score'
    api_key = '56rLiF4ai3eyN8H5fb3WPGDcvfhCV4Pj' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    
    req = urllib.request.Request(url, body, headers)
    
    htmlstr="<html><body>"
    
    try:
        response = urllib.request.urlopen(req)
    
        result = json.loads(response.read())
        htmlstr=htmlstr+"依據您輸入的參數，經過數據分析模型比對，罹患糖尿病的結果為"
        htmlstr=htmlstr+str(result['Results']['WebServiceOutput0'][0]['Scored Probabilities'])
        # print(result)
    
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
    
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
    
    htmlstr=htmlstr+"</body></html>"
    
    return htmlstr

@app.route('/<name>')
def hello(name):
    return "Hello," + name + "!!!" 

if __name__=="__main__":
    app.run()