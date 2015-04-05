# Tumblr reblog data with Python and SQLite

This is a remake of Bellisk's tumblr scraping repo that uses sqlite instead of neo4j.
The original which uses Neo4j can be found [here](https://github.com/bellisk/tumblrgraphing/blob/master/tumblr_graphing.py)

## Usage
You will need sqlite3 in order to use this script.
Run the script from the terminal with `python tumblr_parser.py [URL of post]`.

Data is saved to a `notes` table with the `reblogger` and `source` attributes.
The original poster will have a `source` value of `none`.
