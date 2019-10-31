import requests, json, os
from flask import Flask

app = Flask(__name__)
versionNum = os.getenv('API_VERSION', '1.0.0')

githubURL = 'https://api.github.com/graphql'
OAuthKey = os.getenv('GITHUB_API_KEY')
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

@app.route('/', methods=['GET'])
def index():
    responseData = {"version": versionNum}
    return json.dumps(responseData), 200

@app.route('/repositories', methods=['GET'])
def getAll():
    response = requests.post(githubURL, data=requestData, headers=requestHeaders)

    if response.status_code != 200:
        responseData = {"error": "failed to fetch data", "errorcode": response.status_code}
        return json.dumps(responseData), 404

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
