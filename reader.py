import json
import re
import random


class CAH(dict):
    def __init__(self, file):
        super(CAH, self).__init__()
        with open(file) as f:
            game_json = json.load(f)
            for deck_id, deck in game_json["decks"].items():
                white_cards = [
                    WhiteCard(game_json["cards"]["white"][i]) for i in deck["white"]
                ]
                black_cards = [
                    BlackCard(game_json["cards"]["black"][i]) for i in deck["black"]
                ]
                self[deck_id] = Deck(
                    deck_id,
                    white_cards,
                    black_cards,
                    deck["official"],
                    deck["description"],
                    deck["name"],
                )

    def __str__(self):
        return "Num decks: {} | white: {:4} | black : {:4}".format(
            len(self),
            sum([len(d.white_cards) for d in self.values()]),
            sum([len(d.black_cards) for d in self.values()]),
        )

    def get_white(self, decks=None):
        if decks == None:
            decks = self.values()
        else:
            decks = [x for x in self.values() if x.name in decks]
        return [card for deck in decks for card in deck.white_cards]

    def get_black(self, decks=None):
        if decks == None:
            decks = self.values()
        else:
            decks = [x for x in self.values() if x.name in decks]
        return [card for deck in decks for card in deck.black_cards]


class Deck:
    def __init__(self, id, white_cards, black_cards, official, description, name):
        self.id = id
        self.white_cards = white_cards
        self.black_cards = black_cards
        self.official = bool(official)
        self.description = description
        self.name = name

    def __str__(self):
        return "{:15} | white: {:3} | black: {:3} | {:1} | {}".format(
            self.id,
            len(self.white_cards),
            len(self.black_cards),
            self.official,
            self.name,
        )


class WhiteCard:
    def __init__(self, json_card):
        self.text = json_card["text"]

    def __str__(self):
        return self.text


class BlackCard:
    def __init__(self, json_card):
        self.pick = int(json_card["pick"])
        assert self.pick < 4, json_card
        self.text = json_card["text"]
        self.blanks = [match.start() for match in re.finditer("_", self.text)]
        assert self.pick == 1 or self.pick == len(self.blanks), json_card

    def __str__(self):
        return self.text


def _one_round(game):
    print("{}\n".format(random.choice(game["Base"].black_cards)))
    for i in range(10):
        print("{}: {}".format(i, random.choice(game["Base"].white_cards)))


if __name__ == "__main__":
    file = "data/json-against-humanity/compact.md.json"

    game = CAH(file)
    print(game)

    for deck in game.values():
        print(deck)

    print("\n* Ten random black cards:")
    for i in range(10):
        print("{}: {}=END=".format(i, random.choice(game["Base"].black_cards)))

    print("\n* Ten random white cards:")
    for i in range(10):
        print("{}: {}=END=".format(i, random.choice(game["Base"].white_cards)))

    print("\n\n* And one round:")
    _one_round(game)
