# snootybird.net

The Snooty Bird Publishing website: a single page about the book *What We
Drink*. It is a small Flask app, deployed to Heroku on the `heroku-26` stack.

## Development

```sh
uv sync
uv run flask --app snootybird run --debug
uv run pytest
```

## Deployment

Heroku's Python buildpack installs from `uv.lock`, uses the Python version in
`.python-version`, and runs the `web` process in `Procfile`.

```sh
heroku create snootybird --stack heroku-26   # or, for an existing app:
heroku stack:set heroku-26 -a <app>
git push heroku main
```
