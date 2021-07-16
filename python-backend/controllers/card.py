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
        if cards:
            return jsonify(code=200, cards=list(cards))
        return jsonify(code=400, message='no valid cards has been found for queried user')

    def remove_card(self, card_id, token):
        card = Card()
        is_card_removed = card.remove_card(card_id, token)
        if is_card_removed:
            return jsonify(code=204, message='Card has been removed')

        return jsonify(code=400, message='The operation has not been permitted')

    def add_card(self, new_card, token):
        if token:
            card_model = Card()
            added_card_id = card_model.add_card(new_card, token)
            if added_card_id:
                return jsonify(code=201, new_card_id=added_card_id)

        return jsonify(code=400, message='The new card has not been created')

    def update_card(self, card_id, card, token):
        card_model = Card()
        updated_card = card_model.update_card(card_id, card, token)
        if updated_card:
            return jsonify(code=200, updated_card=updated_card)

        return jsonify(code=400, message='The card has not been updated')
