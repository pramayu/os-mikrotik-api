import bcrypt

def bcrypt_en(plaintext):
	plaintext = plaintext.encode('utf-8')
	hashedtxt = bcrypt.hashpw(plaintext, bcrypt.gensalt(12))
	return hashedtxt