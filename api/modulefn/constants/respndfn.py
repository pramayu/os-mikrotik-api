def def_response(topath, status=False, messag='failed'):
	response = {
		'status': status,
		'messag': messag,
		'topath': topath
	}

	return response