# atlas-service
Search anything.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/atilatech/atlas-service)

For a tutorial on how this service works, see the [Deploy Whisper and Sentence Transformer Model to HuggingFace notebook](notebooks/deploy_whisper_and_sentence_transformer_to_huggingface.ipynb) or open it in a Colab: <a href="https://colab.research.google.com/github/atilatech/atlas-service/blob/master/notebooks/deploy_whisper_and_sentence_transformer_to_huggingface.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Quickstart

TODO: Getting weird import errors when trying to import sibling directories.

`pipenv run python src/app.py`
`ModuleNotFoundError: No module named 'atlas'`

Temporary workaround: use `sls wsgi serve --config serverless.dev.yml`. 

1. `cp serverless.yml serverless.dev.yml`
2. Set the following environment variables:
```yaml
  environment:
    HUGGING_FACE_URL: ""
    HUGGING_FACE_API_KEY: ""
    PINECONE_API_KEY: ""
```
3. `sls wsgi serve --config serverless.dev.yml`
Make sure to put the credentials in serverless.dev.yml and not `serverless.yml`

```bash
pip install pipenv
pipenv install
pipenv run python src/app.py
```

If `pipenv` doesn't work, [try](https://discuss.codecademy.com/t/installing-pipenv-on-a-mac-command-not-found/633353/3)
prefixing all your commands with `python -m pipenv`

```bash
python -m pipenv install
python -m pipenv run python src/app.py
```

### Test the service as a Lambda function locally
To simulate how the lambda sevice will run locally:

`sls wsgi serve`

## Using Gitpod

To set the environment variables in gitpod,
edit the following and paste into your terminal.

```bash
eval $(gp env -e HUGGING_FACE_URL=your_value)
eval $(gp env -e HUGGING_FACE_API_KEY=your_value)
eval $(gp env -e PINECONE_API_KEY=your_value)
```

## Using the API

You can test as a GET request by putting setting the `?url=<url>` and `&q=<search term>` 

Example: https://5000-atilatech-atlasservice-9ogzr6pvij2.ws-us80.gitpod.io/search?url=https://youtu.be/lOI0Gs_t6cQ&q=neural%20network

Since your url might be different you can just copy-paste the following and append it to your API URL.

`/search?q=neural%20network&url=https://youtu.be/lOI0Gs_t6cQ`

To search all videos

`/search?q=throw under the bus`

You can also send POST requests.

```bash
curl --location --request POST 'http://127.0.0.1:5000/search' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://www.youtube.com/watch?v=ciKdF97JWpU",
    "q": "throw under bus"
}'
```
Remove the URL property to search all videos
```bash
curl --location --request POST 'http://127.0.0.1:5000/search' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://www.youtube.com/watch?v=ciKdF97JWpU",
    "q": "throw under bus"
}'
```

## Deployment

1. The service is deployed as an AWS Lambda function
2. View [Function logs in Cloudwatch](https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fatlas-service-prod-app)