# Github Repository Tracker

## How to deploy

1) Create a personal access token on github by following the guide on their website.
2) Add the key as an environment variable on your server under the name GITHUB_API_KEY. (NOTE: docker/kubernetes secrets also work, as long as the variable name is GITHUB_API_KEY)
3) Add the following docker image to your chosen container orchestrator: nemjit001/github-repo-tracker:latest

## Endpoints + return:
### /repositories
```json
{
    "login": "<your login name>",
    "name": "<your name>",
    "repositories": [
        {
            "name": "<repo-name>",
            "url": "<repo-url>",
            "description": "<repo-description>",
            "isPrivate": "false",
            "id": "<repo-id>"
        }
    ]
}
```

### /contributed
```json
{
    "login": "<your login name>",
    "name": "<your name>",
    "repositoriesContributedTo": [
        {
            "nameWithOwner": "<repo-name with owner>",
            "url": "<repo-url>",
            "description": "<repo-description>",
            "id": "<repo-id>",
            "name": "<repo-name>"
        }
    ]
}
```

### /organizations
```json
{
    "login": "<your login name>",
    "name": "<your name>",
    "repositoriesContributedTo": [
        {
            "isVerified": "<wether your company is verified on github>",
            "url": "<repo-url>",
            "description": "<repo-description>",
            "id": "<repo-id>",
            "name": "<repo-name>"
        }
    ]
}
```

## Authors
- Tijmen Verhoef, [Portfolio](https://tverhoef.com)
