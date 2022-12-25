# atlas-service
Search anything.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/atilatech/atlas-service)

## Quickstart

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

## Using Gitpod

To set the environment variables in gitpod,
edit the following and paste into your terminal.

```bash
eval $(gp env -e HUGGING_FACE_URL=your_value)
eval $(gp env -e HUGGING_FACE_API_KEY=your_value)
eval $(gp env -e PINECONE_API_KEY=your_value)
```
