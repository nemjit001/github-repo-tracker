import requests, json, os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OAuthKey = ""

if (os.getenv('GITHUB_API_KEY', None) == None):
    if (os.getenv('GITHUB_API_KEY_FILE', None) != None):
        f = open(os.getenv('GITHUB_API_KEY_FILE'), 'r')
        OAuthKey = f.read()
        f.close()
else:
    OAuthKey = os.getenv('GITHUB_API_KEY')

githubURL = 'https://api.github.com/graphql'
requestHeaders = {'Authorization': f'bearer {OAuthKey}'}
requestData = " \
{ \
    \"query\": \"query { \
        viewer { \
            repositories(first: 100, affiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) { \
                totalCount \
                nodes { \
                    name \
                    url \
                    description \
                    isPrivate \
                    id \
                } \
            } \
            login \
            name \
        } \
    } \" \
} \
"

@app.route('/repositories', methods=['GET'])
def getAll():
    response = requests.post(githubURL, data=requestData, headers=requestHeaders)

    if response.status_code != 200:
        responseData = {"error": "failed to fetch data", "errorcode": response.status_code}
        return json.dumps(responseData), response.status_code

    serverResponse = response.json()
    viewerData = serverResponse['data']['viewer']
    repositoryData = serverResponse['data']['viewer']['repositories']['nodes']

    responseData = { "login": viewerData['login'], "name": viewerData['name'], "repositories": [] }

    for element in repositoryData:
        if not element['isPrivate']:
            responseData['repositories'].append(element)

    return json.dumps(responseData), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
