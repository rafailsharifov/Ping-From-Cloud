import requests

def sms(to, text):

    for to in to:
        url = "https://api.msm.az/sendsms"

        xml = """<?xml version="1.0" encoding="utf-8"?><SMS-InsRequest><CLIENT user="username" pwd="password" from="Company" /><INSERT to="{}" text="{}" /></SMS-InsRequest>""".format(to, text)

        headers = {'Content-Type': 'text/xml', 'content-length': str(len(xml))}
        requests.post(url, data=xml, headers=headers)

    print("I sent sms")
~
