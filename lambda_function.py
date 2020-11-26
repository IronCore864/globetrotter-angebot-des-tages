from datetime import date

import requests
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import ClientError

AWS_REGION = "eu-central-1"


def parse_details():
    URL = 'https://www.globetrotter.de/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='whatsapp-broadcast')

    image_url = results['data-attachement']
    old_price = results['data-oldprice']
    sale_price = results['data-saleprice']
    product_link = results['data-productlink']
    product_name = results['data-productname']

    return """<a href="{}">
        <img src="{}">
        <p>{}</p>
        <p>Original price: {}</p>
        <p>Now: {}</p>
    </a>""".format(
        product_link,
        image_url,
        product_name,
        old_price,
        sale_price
    )


def build_subject():
    today = date.today()
    return "Angebot des Tages - Globetrotter - {}".format(today)


def build_body_text_html():
    angebot_details = parse_details()
    return """Amazon Pinpoint Test (SDK for Python)
    -------------------------------------
    This email was sent with Amazon Pinpoint using the AWS SDK for Python (Boto 3).
    For more information, see https:#aws.amazon.com/sdk-for-python/
    """, """<html>
    <head></head>
    <body>
        {}
    </body>
</html>
    """.format(angebot_details)


def handler(event, context):
    SENDER = "info <noreply@guotiexin.com>"
    RECIPIENT = "guotiexin@gmail.com"
    SUBJECT = build_subject()
    BODY_TEXT, BODY_HTML = build_body_text_html()
    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


if __name__ == "__main__":
    handler(None, None)
