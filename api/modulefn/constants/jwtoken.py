import jwt
from os import path
from datetime import datetime, timedelta

def encode_payload(data, status):
	key = open(path.join('api/modulefn/secretfile/jwtRS256.key'), 'r').read()
	payload = {
		"_id": data['_id'], "nickname": data['nickname'], "uid": "" if status == True else data['uid'],
		"exp": datetime.utcnow() + timedelta(days=7) if status == True else datetime.utcnow() + timedelta(hours=24)
	}
	encode = jwt.encode(payload, key, algorithm='RS256')
	return encode

def decode_token(token):
	public = open(path.join('api/modulefn/secretfile/jwtRS256.key.pub'), 'r').read()
	decode = jwt.decode(token, public, algorithms=['RS256'], options={
		"verify_signature": True,
		"verify_exp": True})
	return decode

def chr_api(transaction):
	key = open(path.join('api/modulefn/secretfile/jwtRS256.key'), 'r').read()
	payload = {
		'transaction_status': transaction, 'exp': datetime.utcnow() + timedelta(minutes=25)
	}
	encode = jwt.encode(payload, key, algorithm='RS256')
	return encode

def encode_router(data):
	key = open(path.join('api/modulefn/secretfile/jwtRS256.key'), 'r').read()
	payload = {
		'_id': data['rtrconfid'], 'user': data['username']
	}
	encode = jwt.encode(payload, key, algorithm='RS256')
	return encode