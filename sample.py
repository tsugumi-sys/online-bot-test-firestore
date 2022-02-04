import os
import urllib

import google.auth.transport.requests
import google.oauth2.id_token

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./online-bot-test-backend-service-account.json"


def make_authorized_get_request(service_url):
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    in service_url (must be a complete URL) by authenticating with the
    ID token obtained from the google-auth client library.
    """

    req = urllib.request.Request(service_url)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)

    return response.read()


service_url = "https://online-bot-test-rlvpeusr2a-uc.a.run.app/docs/"

res = make_authorized_get_request(service_url)
print(res)
