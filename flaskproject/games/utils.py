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

