from flask_inertia import Inertia
import json
from flask import session, request
from flask_login import current_user

# Initialize Inertia-Flask
inertia = Inertia()

def init_inertia(app):
    """Initialize Inertia with the Flask app"""
    inertia.init_app(app)
    
    # Configure Inertia
    app.config["INERTIA_TEMPLATE"] = "inertia.html"
    
    # Add shared data for authentication
    def share_auth():
        if current_user.is_authenticated:
            # Get unread message count
            unread_count = 0
            if hasattr(current_user, 'notifications'):
                unread_count = current_user.notifications.filter_by(read_status=False, type='message').count()
                
            return {
                'auth': {
                    'user': {
                        'id': current_user.id,
                        'email': current_user.email,
                        'user_type': current_user.user_type,
                    },
                    'unread_count': unread_count
                }
            }
        return {'auth': None}
        
    inertia.share(share_auth)
    
    # Flash messages middleware
    @app.before_request
    def share_flash_messages():
        from flask import get_flashed_messages as flash_msgs
        messages = []
        for category, message in flash_msgs(with_categories=True):
            messages.append({
                'type': category,
                'message': message
            })
        
        # Share flash messages with Inertia
        inertia.share({'flash': messages})