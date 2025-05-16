from flask import session, request, jsonify, render_template, make_response, g
from flask_login import current_user
import json

class CustomInertia:
    """A simplified Inertia implementation for Flask"""
    
    def __init__(self):
        self.shared_data = {}
    
    def share(self, key, value=None):
        """Share data across all Inertia responses"""
        if callable(key) and value is None:
            self.shared_data.update(key())
        elif isinstance(key, dict) and value is None:
            self.shared_data.update(key)
        else:
            self.shared_data[key] = value
    
    def render(self, component_name, props=None, version=None):
        """Render an Inertia-powered page"""
        if props is None:
            props = {}
        
        # Merge shared data with page props
        merged_props = {**self.shared_data, **props}
        
        page_data = {
            'component': component_name,
            'props': merged_props,
            'url': request.path,
            'version': version or '1'
        }
        
        # Handle Inertia requests (XHR/fetch)
        if 'X-Inertia' in request.headers and request.headers['X-Inertia'] == 'true':
            response = make_response(jsonify(page_data))
            response.headers['X-Inertia'] = 'true'
            response.headers['Vary'] = 'Accept'
            return response
        
        # Handle regular page loads
        return render_template('inertia.html', page=page_data)

# Create a global instance of our CustomInertia
inertia = CustomInertia()

def init_inertia(app):
    """Initialize Inertia with the Flask app"""
    # Configure Inertia
    app.config["INERTIA_TEMPLATE"] = "inertia.html"
    
    # Middleware to gather auth data and flash messages before each request
    @app.before_request
    def prepare_inertia_data():
        # Auth data
        auth_data = {}
        if current_user.is_authenticated:
            # Get unread message count
            unread_count = 0
            if hasattr(current_user, 'notifications'):
                try:
                    unread_count = current_user.notifications.filter_by(read_status=False, type='message').count()
                except:
                    unread_count = 0
                
            auth_data = {
                'auth': {
                    'user': {
                        'id': current_user.id,
                        'email': current_user.email,
                        'user_type': current_user.user_type,
                    },
                    'unread_count': unread_count
                }
            }
        else:
            auth_data = {'auth': None}
        
        # Flash messages
        from flask import get_flashed_messages as flash_msgs
        messages = []
        for category, message in flash_msgs(with_categories=True):
            messages.append({
                'type': category,
                'message': message
            })
        
        flash_data = {'flash': messages}
        
        # Share data with Inertia
        inertia.share(auth_data)
        inertia.share(flash_data)