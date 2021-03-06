import jwt
import datetime


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    print("Making token")
    secret_key="hi_everyone"
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=432000),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            #app.config.get('SECRET_KEY'),
            secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    secret_key = "hi_everyone"
    try:
        payload = jwt.decode(auth_token,secret_key)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'