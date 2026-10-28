from flask import Flask, render_template, request, send_from_directory
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

    @app.route("/")
    def index():
        return render_template("index.html", spread_pages=SPREAD_PAGES)

    @app.route("/favicon.ico")
    @app.route("/robots.txt")
    def root_static():
        return send_from_directory(app.static_folder, request.path.lstrip("/"))

    return app
