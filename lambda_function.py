import requests
from bs4 import BeautifulSoup
import json
import datetime

def find_title(schema_data):
    rv = ''
    if 'headline' in schema_data:
        rv = schema_data['headline']
    return rv

def find_author(schema_data):
    rv = ''
    schema_data = schema_data
    if 'author' in schema_data:
        author = schema_data['author']
        if 'name' in author:
            rv = author['name']
        else:
            rv = author[0]['name']
        rv = rv.split(' ')
        if len(rv) == 2:
            rv.insert(1, '')
        while (len(rv) < 4):
            rv.append('')
    return rv

def find_website_title(schema_data):
    rv = ''
    if 'publisher' in schema_data:
        publisher = schema_data['publisher']
        if 'name' in publisher:
            rv = publisher['name']
    return rv

def find_date_published(schema_data):
    rv = ''
    if 'datePublished' in schema_data:
        rv = schema_data['datePublished']
        rv = rv[0:rv.index('T')]
        rv = rv.split('-')
        for i in range(len(rv)):
            rv[i] = int(rv[i])
    return rv

def find_date_accessed():
    today = datetime.date.today()
    rv = [today.year, today.month, today.day]
    return rv


def lambda_handler(event, context):
    url = event['queryStringParameters']['url']

    url = url.replace("%3A", ":")
    url = url.replace("%2F", "/")

    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    schema_tags = soup.find_all('script', {'type': 'application/ld+json'})

    title = ''
    author = ['']
    website_title = ''
    date_published = ''
    date_accessed = find_date_accessed()

    for tag in schema_tags:
        tagStr = tag.string.strip()
        while not tagStr[-1] == '}':
            tagStr = tagStr[:-1]
        schema_data = json.loads(tagStr)
        title_check = find_title(schema_data)
        if not title_check == '':
            title = title_check
        author_check = find_author(schema_data)
        if not author_check == '':
            author = author_check
        website_title_check = find_website_title(schema_data)
        if not website_title_check == '':
            website_title = website_title_check
        date_published_check = find_date_published(schema_data)
        if not date_published_check == '':
            date_published = date_published_check

    if ' '.join(author) == website_title:
        author.clear()

    data = {
        'url': url,
        'title' : title,
        'author' : author,
        'publisher' : ['','','',''],
        'website_title' : website_title,
        'date_published' : date_published,
        'date_accessed' : date_accessed
    }

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Credentials": True
        },
        'body': json.dumps(data)
    }