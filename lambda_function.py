import json
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
from flask_cors import CORS
from flask import Flask, request, jsonify
app = Flask(__name__)
CORS(app)
@app.route('/script', methods=['POST'])

def lambda_handler():
    p = request.json
    new_json = {
        "id": "ITEM",
        "type": "webpage",
        "title": p["title"],
        "container-title": p["website_title"],
        "author": [
            {
            "family": p["author"][2],
            "given": p["author"][0]
            }
        ],
        "issued": {
            "date-parts": [
                p["date_published"]
            ]
        },
        "URL": p["url"],
        "accessed": {
            "date-parts": [
                p["date_accessed"]
            ]
        }
    }
    json_input = json.dumps(new_json)

    json_data = [json.loads(json_input)]
    bib_source = CiteProcJSON(json_data)
    bib_style = CitationStylesStyle('modern-language-association.csl', validate=False)
    bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.html)
    citation1 = Citation([CitationItem('ITEM')])
    bibliography.register(citation1)
    rv = ''
    for item in bibliography.bibliography():
        rv = rv+ (str(item))
    print(rv)
    return {
        'statusCode': 200,
        'body': json.dumps(rv)
    }

if __name__ == '__main__':
    app.run(port=5000)