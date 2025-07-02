from google.auth.transport import requests
from google.oauth2 import id_token
from fastapi import HTTPException
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

def verify_google_token(token: str):
    """Verify Google OAuth token and return user info"""
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID
        )
        
        # If the token is valid, return user info
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
            
        return {
            'email': idinfo['email'],
            'name': idinfo.get('name', ''),
            'picture': idinfo.get('picture', ''),
            'google_id': idinfo['sub']
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token verification failed: {str(e)}")