import http.client
import sys
import gzip
import json


def spell_check(text):
    conn = http.client.HTTPSConnection("orthographe.reverso.net")
    payload = json.dumps(
        {
            "englishDialect": "indifferent",
            "autoReplace": True,
            "getCorrectionDetails": True,
            "interfaceLanguage": "en",
            "locale": "",
            "language": "eng",
            "text": text,
            "originalText": "",
            "origin": "ginger.web",
            "isHtml": False,
            "IsUserPremium": False,
        }
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "text/json",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/*+json",
        "Connection": "keep-alive",
    }

    conn.request("POST", "/api/v1/Spelling/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    decoded_data = gzip.decompress(data).decode("utf-8")
    json_data = json.loads(decoded_data)

    return json_data["text"]


if __name__ == "__main__":
    ALFRED_QUERY = " ".join(sys.argv[1:])
    sys.stdout.write(spell_check(ALFRED_QUERY))
