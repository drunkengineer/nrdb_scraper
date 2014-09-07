import sys
import time

import parse_html


def main():
    """Manipulates and outputs data related to NetrunnerDB Hall of Fame."""
    decks = parse_html.main()
    decks = sort_by_date(decks)
    output_decks(decks)
    users = sort_by_most_rep(decks)
    output_users(users)


def sort_by_likes(decks):
    return sorted(decks, key=lambda l: l[0], reverse=True)


def sort_by_faves(decks):
    return sorted(decks, key=lambda l: l[1], reverse=True)


def sort_by_comments(decks):
    return sorted(decks, key=lambda l: l[2], reverse=True)


def sort_by_name(decks):
    return sorted(decks, key=lambda l: l[3].lower())


def sort_by_user(decks):
    return sorted(decks, key=lambda l: l[5].lower())


def sort_by_rep(decks):
    return sorted(decks, key=lambda l: l[6], reverse=True)


def sort_by_date(decks):
    return sorted(decks, key=lambda l: l[7], reverse=True)


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


def sort_by_most_decks(decks):
    user_dict = most_prolific_users(decks)
    return sorted(user_dict.items(), key=lambda l: l[1], reverse=True)


def sort_by_most_rep(decks):
    user_dict = most_prolific_users(decks)
    return sorted(user_dict.items(), key=lambda l: l[1][1], reverse=True)


def most_prolific_users(decks):
    """Retrieves rep and number of decks in Hall of Fame for each user"""
    users = {}
    decks = sort_by_user(decks)
    for deck in decks:
        user = deck[5]
        if not user in users:
            users[user] = [1, int(deck[6])]
        else:
            users[user][0] += 1
    return users


def output_users(users):
    """Prints readable list of users by rep or number of decks"""
    transpose_users = [list(i) for i in zip(*users)]
    longest_user = len(max(transpose_users[0], key=len))

    print("User".ljust(longest_user), "Decks".rjust(5), "Rep".rjust(4))
    print("-"*longest_user, "-"*5, "-"*4)
    for user in users:
        print(user[0].ljust(longest_user), str(user[1][0]).rjust(5), str(user[1][1]).rjust(4))


if __name__ == '__main__':
    sys.exit(main())