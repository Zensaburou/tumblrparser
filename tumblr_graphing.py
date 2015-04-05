# -*- coding: utf-8 -*-

import requests, sys, re, sqlite3
from bs4 import BeautifulSoup

def save_notes_on_page(db, soup):
    cursor = db.cursor()
    for link in soup.find_all("li", "reblog"):
        reblogger = link.select(".tumblelog")[0].string
        try:
            source = link.select(".source_tumblelog")[0].string
        except IndexError:
            source = 'none'
        cursor.execute('''
            INSERT INTO notes(reblogger, source)
            values(?,?)''',(reblogger, source)
        )
        print (reblogger, source)
    db.commit()

def create_db():
    db = sqlite3.connect('data.sqlite3')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE notes(
            id INTEGER PRIMARY KEY,
            reblogger TEXT,
            source TEXT
        )
    ''')
    return db

def get_all_notes(posturl):
    db = create_db()
    r = requests.get(posturl)
    soup = BeautifulSoup(r.text)
    # get notes from front page
    save_notes_on_page(db, soup)

    morenotes = soup.find_all("a", "more_notes_link")
    while morenotes:
        # get notes page url
        regex = u"'(/notes/[\w=?/]*)'"
        blogurl = "/".join(posturl.split("/")[0:3])
        notes_url = blogurl + re.search(regex, str(morenotes[0])).group(1)

        # request and soupify the next page of notes
        r = requests.get(notes_url)
        soup = BeautifulSoup(r.text)
        morenotes = soup.find_all("a", "more_notes_link")

        # get notes from current page
        save_notes_on_page(db, soup)

if __name__ == "__main__":
    posturl = sys.argv[1]
    get_all_notes(posturl)
