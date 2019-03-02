import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
	'''
	Resizes and saves the user picture
	'''

	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext

	picture_path = os.path.join(current_app.root_path, 'static/game_pics',picture_fn)
	output_size = (125,125)

	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


def calculate_elo(p1_elo, p2_elo, winner, k_factor=20):

	esp_score_p1 = 1 / (1 + 10 ** ((p2_elo - p1_elo) / 400))
	esp_score_p2 = 1 / (1 + 10 ** ((p1_elo - p2_elo) / 400))

	if winner is None:
		score_p1 = score_p2 = 0.5

	elif winner:
		score_p1 = 1
		score_p2 = 0

	else:
		score_p1 = 0
		score_p2 = 1

	new_elo_p1 = p1_elo + k_factor * (score_p1 - esp_score_p1)
	new_elo_p2 = p2_elo + k_factor * (score_p2 - esp_score_p2)

	return new_elo_p1, new_elo_p2
