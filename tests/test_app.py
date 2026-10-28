import re

import pytest

from snootybird import SPREAD_PAGES, create_app


@pytest.fixture
def client():
    return create_app({"TESTING": True}).test_client()


def test_front_page(client):
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<title>Snooty Bird Publishing</title>" in html
    assert html.count("custom-indicator") == len(SPREAD_PAGES) + 1


def test_og_image_is_absolute_https_behind_heroku_router(client):
    response = client.get("/", headers={"X-Forwarded-Proto": "https", "X-Forwarded-Host": "snootybird.net"})
    html = response.get_data(as_text=True)
    assert 'content="https://snootybird.net/static/images/snooty-bird-circle-large.png"' in html


def test_every_referenced_static_file_exists(client):
    html = client.get("/").get_data(as_text=True)
    paths = re.findall(r'(?:src|href)="(/static/[^"]+)"', html)
    assert len(paths) > len(SPREAD_PAGES)
    for path in paths:
        assert client.get(path).status_code == 200, path


@pytest.mark.parametrize("path", ["/", "/robots.txt?x=1"])
def test_plain_http_from_heroku_router_redirects_to_https(client, path):
    response = client.get(path, headers={"X-Forwarded-Proto": "http", "X-Forwarded-Host": "www.snootybird.net"})
    assert response.status_code == 301
    assert response.headers["Location"] == f"https://www.snootybird.net{path}"


def test_https_and_local_requests_are_not_redirected(client):
    assert client.get("/", headers={"X-Forwarded-Proto": "https"}).status_code == 200
    assert client.get("/").status_code == 200


@pytest.mark.parametrize("path", ["/favicon.ico", "/robots.txt"])
def test_root_static_files(client, path):
    assert client.get(path).status_code == 200
