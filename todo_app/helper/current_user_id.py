from flask_login import current_user

def get_current_user_id():
    if current_user.is_anonymous:
        return 'anonymous-user'
    
    return current_user.id
