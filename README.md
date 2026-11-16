# snootybird.net

The Snooty Bird Publishing website: a single static page about the book *What We
Drink*, served by GitHub Pages at https://www.snootybird.net.

## Development

The site is the `site/` folder: `index.html` and the files it uses (`static/`).
To look at it locally:

```sh
python3 -m http.server -d site 8000     # then open http://localhost:8000
python3 -m unittest discover -s tests   # every file the page refers to is there
```

## Deployment

Pushing to `main` runs `.github/workflows/pages.yml`: it checks the site, then
publishes `site/` to GitHub Pages (Settings → Pages → Source: GitHub Actions,
custom domain www.snootybird.net with Enforce HTTPS). DNS: `www` is a CNAME to
`jwnichls.github.io`; the bare domain forwards to `https://www.snootybird.net`.
