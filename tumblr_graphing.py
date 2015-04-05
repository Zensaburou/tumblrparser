# -*- coding: utf-8 -*-

import requests, sys, re, sqlite3
from bs4 import BeautifulSoup

def notes_on_page(soup):
    notes_on_page = []
    for reblog in soup.find_all("li", "reblog"):
        notes_on_page.append(reblog.get_text())
    return notes_on_page

def get_all_notes(posturl):
    r = requests.get(posturl)
    soup = BeautifulSoup(r.text)
    reblogs = []

    # get notes from front page
    reblogs + notes_on_page(soup)

    morenotes = soup.find_all("a", "more_notes_link")
    while morenotes:
        # get notes page url
        regex = u"'(/notes/[\w=?/]*)'"
        blogurl = "/".join(posturl.split("/")[0:3])
        notes_url = blogurl + re.search(regex, str(morenotes[0])).group(1)
        print notes_url

        # request and soupify the next page of notes
        r = requests.get(notes_url)
        soup = BeautifulSoup(r.text)
        morenotes = soup.find_all("a", "more_notes_link")

        # get notes from current page
        reblogs + notes_on_page(soup)

    print len(reblogs)
    return reblogs

def write_to_db(reblogs):
    db = sqlite3.connect('data')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE reblogs(
            id INTEGER PRIMARY KEY,
            reblogger TEXT,
            source TEXT
        )
    ''')
    db.commit()

    for reblog in reblogs:
        poster = reblog.select(".tumblelog")[0].string
        source = reblog.select(".source_tumblelog")[0].string
        cursor.execute('''
            INSERT INTO reblogs(reblogger, source)
            VALUES(?,?)''',(poster, source))
        db.commit()
    db.close()

if __name__ == "__main__":
    posturl = sys.argv[1]
    reblogs = get_all_notes(posturl)
    write_to_db(reblogs)
