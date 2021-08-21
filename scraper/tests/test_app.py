from chalice.test import Client
from app import app


def test_app():
    with Client(app) as client:
        event = client.events.generate_cw_event("",'',{},[])
        response = client.lambda_.invoke('scrape_facebook_groups', event)
        print(response)
