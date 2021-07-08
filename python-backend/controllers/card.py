from models.card import Card
from flask import jsonify


class CardController():
    def get_all(self):
        card = Card()
        cards = card.get_all()
        return jsonify(code=200, cards=list(cards))

    def get_all_filtered_by_author(self, author_id):
        card = Card()
        cards = card.get_cards_by_author(author_id)
        return jsonify(code=200, cards=list(cards))

    def remove_card(self, card_id, token):
        card = Card()
        is_card_removed = card.remove_card(card_id, token)
        if is_card_removed:
            return jsonify(code=204, message='Card has been removed')

        return jsonify(code=400, message='The operation has not been permitted')

    def add_card(self, card, token):
        card = Card()
        added_card = card.add_card(card, token)
        if added_card:
            return jsonify(code=201, new_card_id=added_card['_id'])

        return jsonify(code=400, message='The new card has not been created')

    def update_card(self, card_id, card, token):
        card = Card()
        updated_card = card.update_card(card_id, card, token)
        if updated_card:
            return jsonify(code=200, updated_card=updated_card)

        return jsonify(code=400, message='The card has not been updated')
