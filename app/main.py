import requests, json, os, markdown
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OAuthKey = ""

if (os.getenv('GITHUB_API_KEY', None) != None):
    OAuthKey = os.getenv('GITHUB_API_KEY')

if (os.getenv('GITHUB_API_KEY_FILE', None) != None):
    f = open(os.getenv('GITHUB_API_KEY_FILE'), 'r')
    OAuthKey = f.readline().replace('\n', '')
    f.close()

githubURL = 'https://api.github.com/graphql'
requestHeaders = {'Authorization': f'bearer {OAuthKey}'}

def getRequestData(filepath):
    requestFile = open(filepath, 'r')
    requestData = requestFile.read()
    requestFile.close()

    return requestData

@app.route('/', methods=['GET'])
def home():
    md_file = open('README.md', 'r')
    data = md_file.read()
    md_file.close()
    return markdown.markdown(data)

@app.route('/organizations', methods=['GET'])
def getOrganizations():
    requestData = getRequestData('app/companyRequest.json')
    response = response = requests.post(githubURL, data=requestData, headers=requestHeaders)

    if response.status_code != 200:
        responseData = {"error": "failed to fetch data", "errorcode": response.status_code}
        return responseData, response.status_code

    serverResponse = response.json()
    viewerData = serverResponse['data']['viewer']
    repositoryData = serverResponse['data']['viewer']['organizations']['nodes']

    responseData = { "login": viewerData['login'], "name": viewerData['name'], "organizations": repositoryData }

    return responseData, 200

@app.route('/contributed')
def getContributed():
    requestData = getRequestData('app/contributionRequest.json')
    response = requests.post(githubURL, data=requestData, headers=requestHeaders)

    if response.status_code != 200:
        responseData = {"error": "failed to fetch data", "errorcode": response.status_code}
        return responseData, response.status_code

    serverResponse = response.json()
    viewerData = serverResponse['data']['viewer']
    repositoryData = serverResponse['data']['viewer']['repositoriesContributedTo']['nodes']

    responseData = { "login": viewerData['login'], "name": viewerData['name'], "repositories": [] }

    for element in repositoryData:
        if not element['isPrivate']:
            responseData['repositories'].append(element)

    return responseData, 200

@app.route('/repositories', methods=['GET'])
def getRepositories():
    requestData = getRequestData('app/repositoryRequest.json')
    response = requests.post(githubURL, data=requestData, headers=requestHeaders)

    if response.status_code != 200:
        responseData = {"error": "failed to fetch data", "errorcode": response.status_code}
        return responseData, response.status_code

    serverResponse = response.json()
    viewerData = serverResponse['data']['viewer']
    repositoryData = serverResponse['data']['viewer']['repositories']['nodes']

    responseData = { "login": viewerData['login'], "name": viewerData['name'], "repositories": [] }

    for element in repositoryData:
        if not element['isPrivate']:
            responseData['repositories'].append(element)

    return responseData, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
