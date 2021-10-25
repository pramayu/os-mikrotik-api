import bcrypt

def bcrypt_de(plaintext,hashed):
	pwd = plaintext.encode('utf-8')
	hsh = hashed.encode('utf-8')
	if bcrypt.checkpw(pwd, hsh):
		return True
	else:
		return False