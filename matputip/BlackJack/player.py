from cards import Hand


class Player:
	def __init__(self, is_dealer=False):
		self.type = 'dealer' if is_dealer else 'player'
		self.hand = Hand()

	def hit(self, card):
		self.hand.add_card(card)

	def hand_total(self):
		return self.hand.get_total()

	def show_hand(self, hole_card=False):
		total = self.hand.get_total()
		for n in range(len(self.hand.cards)):
			if self.type == 'dealer' and n == 0 and hole_card:
				print('{num}) {val}'.format(num=n, val='–'))
				continue

			val = self.hand.cards[n].value
			print('{num}) {val}'.format(num=n, val=val))

		if self.type == 'player' or not hole_card:
			print('Total: {total}'.format(total=total))

	def __str__(self):
		return 'Player Type: ' + self.type + '\n'
