# Web API for Fact Finder app

# Imports
import flask
from flask import request, jsonify
import wikipedia
import wikipediaapi


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Default page
@app.route('/', methods=['GET'])
def home():
    return "<h1>Willy's Fact Finder Web API<h1><p>Send some GET requests for some Wiki scrapings!</p>"


# Search requests shall be routed through here
# URL format should be www.blahblahblah.com/api/scrape?item=something_like_this
# The information after 'item=' being the search (include underscores between words)
@app.route('/api/scrape', methods=['GET'])
def find_facts():
    # Make sure request has information in it
    if 'item' in request.args:
        item = str(request.args['item'])
    else:
        return "Error: No item field provided. Specify a search term!"

    # Turn URL format item into a searchable term
    search = item.replace("_", " ")

    # Hunt for the most viable search option
    potential = wikipedia.search(search, results=3)
    if potential:
        search = potential[0]
    else:
        return "No such page exists, try again!"

    # Scrape the most valid page for information
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(search)

    return jsonify(page.summary)


app.run()
