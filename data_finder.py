from flask import Flask, request, render_template, url_for
app = Flask(__name__)
import os, json
import requests

@app.route("/", methods=['GET'])
def home():
    base = []
    client_id  = os.environ['CLIENT_ID'] #api3 client id
    client_secret = os.environ['CLIENT_SECRET'] #api3 secret
    client_api_host = os.environ['CLIENT_API_HOST'] #i.e https://<yourlookhost>:19999/api/3.0
    auth_data = {'client_id':client_id, 'client_secret':client_secret}
    r = requests.post(client_api_host + "/login" ,data=auth_data)
    json_auth = r.json()
    all_models = requests.get(client_api_host + '/lookml_models?fields=name,explores', headers={'Authorization': "token " + json_auth['access_token']})
    for model in all_models.json():
        for explore in model['explores']:
            explore_url = client_api_host + '/lookml_models/{0}/explores/{1}?fields=fields(dimensions(name,label_short,description))'.format(model['name'],explore['name'])
            explore_info = requests.get(explore_url, headers={'Authorization': "token " + json_auth['access_token']})
            for dim in explore_info.json()['fields']['dimensions']:
                base.append({"name":dim['name'],"label":dim['label_short'],"description":dim['description']})
    return render_template('index.html', datadict=base)

if __name__ == "__main__":
    app.run(debug=True)
