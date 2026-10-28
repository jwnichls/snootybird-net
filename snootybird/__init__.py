from flask import Flask, redirect, render_template, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

# The book carousel shows the cover followed by these spread pages
SPREAD_PAGES = range(1, 38)


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)

    # Heroku's router terminates TLS, so trust its forwarded scheme and host
    # when building absolute URLs (e.g. the og:image meta tag)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Heroku doesn't redirect plain HTTP itself; its router marks those
    # requests, so send them to HTTPS (local development has no such header)
    @app.before_request
    def redirect_to_https():
        if request.headers.get("X-Forwarded-Proto") == "http":
            return redirect(request.url.replace("http://", "https://", 1), code=301)

    @app.route("/")
    def index():
        return render_template("index.html", spread_pages=SPREAD_PAGES)

    @app.route("/favicon.ico")
    @app.route("/robots.txt")
    def root_static():
        return send_from_directory(app.static_folder, request.path.lstrip("/"))

    return app
