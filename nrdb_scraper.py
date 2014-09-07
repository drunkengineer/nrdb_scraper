import getopt
import sys
import time

from parse_html import parse_html
import sort


def main(argv):
    """Manipulates and outputs data related to NetrunnerDB Hall of Fame."""
    valid_deck_args = "<likes|faves|comments|name|user|rep|date>"
    valid_user_args = "<decks|rep>"
    help_msg = "nrdb_scraper.py -d " + valid_deck_args + " -u " + valid_user_args
    invalid_arg = "Invalid argument:"
    valid_args_are = "Valid args are:"

    try:
        opts, args = getopt.getopt(argv, "hd:u:", ["decks=", "users="])
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_msg)
            sys.exit()
        else:
            decks = parse_html()
            if opt in ("-d", "--decks"):
                try:
                    decks = getattr(sort, "sort_by_" + arg)(decks)
                    output_decks(decks)
                except AttributeError:
                    print(invalid_arg, '"' + opt, arg + '"')
                    print(valid_args_are, valid_deck_args)
                    sys.exit()
            if opt in ("-u", "--users"):
                try:
                    users = getattr(sort, "sort_by_most_" + arg)(decks)
                    output_users(users)
                except AttributeError:
                    print(invalid_arg, '"' + opt, arg + '"')
                    print(valid_args_are, valid_user_args)
                    sys.exit()


def output_decks(decks):
    """Prints readable list of decks."""
    transpose_decks = [list(i) for i in zip(*decks)]
    longest_deck = len(max(transpose_decks[3], key=len))
    longest_user = len(max(transpose_decks[5], key=len))

    print("Deck".ljust(longest_deck), "L".center(3), "F".center(3), "C".center(3), "User".ljust(longest_user),
          "Date".ljust(10))
    print("-"*longest_deck, "-"*3, "-"*3, "-"*3, "-"*longest_user, "-"*10)
    for deck in decks:
        print(deck[3].ljust(longest_deck), str(deck[0]).rjust(3), str(deck[1]).rjust(3), str(deck[2]).rjust(3),
              deck[5].ljust(longest_user), time.strftime("%Y-%m-%d", deck[7]))


def output_users(users):
    """Prints readable list of users by rep or number of decks"""
    transpose_users = [list(i) for i in zip(*users)]
    longest_user = len(max(transpose_users[0], key=len))

    print("User".ljust(longest_user), "Decks".rjust(5), "Rep".rjust(4))
    print("-"*longest_user, "-"*5, "-"*4)
    for user in users:
        print(user[0].ljust(longest_user), str(user[1][0]).rjust(5), str(user[1][1]).rjust(4))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))