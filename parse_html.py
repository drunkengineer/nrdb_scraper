import calendar
from datetime import datetime
import time
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen


def parse_html():
    """Retrieves Hall of Fame data from NetrunnerDB and turns it into a 2D list."""
    decks = []
    url = "http://netrunnerdb.com/en/decklists/halloffame/"
    url_page = 1
    while check_for_decks(url + str(url_page)):
        parse_hall_of_fame(decks, url + str(url_page))
        url_page += 1
    decks = add_deck_dates(decks)
    return decks


def get_soup(url):
    """Strips html of non-deck data."""
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    soup = soup.get_text().split("«")[1].split("»")[1]
    soup = conv_unicode(soup)
    return soup


def conv_unicode(soup):
    """Replace non-unicode characters with unicode"""
    soup = soup.replace("–", "-")
    return soup


def check_for_decks(url):
    """Confirms that there are decks in page."""
    soup = get_soup(url)
    return soup.rstrip("\n") != ""


def parse_hall_of_fame(decks, url):
    """Converts text to decks list."""
    soup = get_soup(url)
    soup = strip_whitespace(soup)
    for deck in soup:
        output = []
        deck = deck.split("\n")
        likes = int(deck[0])
        faves = int(deck[1])
        comments = int(deck[2])
        name = deck[3:-3][0]
        date = deck[-3]
        user = deck[-2]
        rep = int(deck[-1])
        output.extend((likes, faves, comments, name, date, user, rep))
        decks.append(output)
    return decks


def strip_whitespace(soup):
    """Removes tabs and extra newlines from html."""
    soup = soup.replace("\t", "")
    loops = 3  # The number of loops that puts a double line between decks and a single line between elements of a deck
    for i in range(loops):
        soup = soup.replace("\n\n", "\n")
    soup = soup.lstrip("\n\n").rstrip("\n\n").split("\n\n")
    return soup


def parse_hall_of_fame_manual(filename):
    """
    Return list of decks retrieved by manually copying and pasting from NetrunnerDB and stripping header and footer.
    Data must be in the form:
    <Likes> <Faves> <Comments> <Name>
    <Month> <Day> <User> <Rep>
    <Blank Line>
    """

    decks = []
    deckrow = 0
    with open(filename) as f:
        for line in f:
            line = line.split()

            if line:
                if line[0].isdigit():  # First line of deck
                    likes = int(line[0])
                    faves = int(line[1])
                    comments = int(line[2])
                    name = " ".join(line[3:])

                    decks.append([])
                    decks[deckrow].extend((likes, faves, comments, name))

                else:  # Second line of deck
                    date = " ".join(line[0:2])
                    user = " ".join(line[2:-1])
                    rep = int(line[-1])

                    decks[deckrow].extend((date, user, rep))

            else:
                deckrow += 1

    decks = add_deck_dates(decks)
    return decks


def add_deck_dates(decks):
    """Parses date of deck and appends it to deck array."""
    today = datetime.now()
    for deck in decks:
        date_string = deck[4] + " "
        decktime = time.strptime(date_string + str(today.year), "%b %d %Y")
        if calendar.timegm(decktime) > time.mktime(today.timetuple()):
            decktime = time.strptime(date_string + str(today.year - 1), "%b %d %Y")
        deck.append(decktime)
    return decks


if __name__ == '__main__':
    sys.exit(parse_html())