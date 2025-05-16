from flask import request, render_template, jsonify, make_response
from flask_login import current_user
import json

class SimpleInertia:
    """A simple Inertia implementation for Flask"""
    
    def __init__(self):
        self.shared_props = {}
    
    def share(self, data):
        """Share data across all Inertia responses"""
        if isinstance(data, dict):
            self.shared_props.update(data)
        else:
            # Handle incorrect input
            pass
    
    def render(self, component_name, props=None, version='1'):
        """Render an Inertia-powered page"""
        if props is None:
            props = {}
        
        # Include authentication info
        auth_data = None
        if current_user.is_authenticated:
            unread_count = 0
            if hasattr(current_user, 'notifications'):
                try:
                    unread_count = current_user.notifications.filter_by(read_status=False, type='message').count()
                except:
                    unread_count = 0
                
            auth_data = {
                'id': current_user.id,
                'email': current_user.email,
                'user_type': current_user.user_type,
                'unread_count': unread_count
            }
        
        # Merge all props
        all_props = {
            **self.shared_props,
            **props,
            'auth': auth_data
        }
        
        # Create page data
        page_data = {
            'component': component_name,
            'props': all_props,
            'url': request.path,
            'version': version
        }
        
        # Return appropriate response
        if 'X-Inertia' in request.headers and request.headers['X-Inertia'] == 'true':
            # API response for Inertia requests
            response = make_response(jsonify(page_data))
            response.headers['X-Inertia'] = 'true'
            response.headers['Vary'] = 'Accept'
            return response
        
        # Regular HTML response
        return render_template('inertia.html', page=page_data)

# Create global instance
inertia = SimpleInertia()

def init_inertia(app):
    """Initialize Inertia with the Flask app"""
    # Configure Inertia
    app.config["INERTIA_TEMPLATE"] = "inertia.html"
    
    # Add flash messages to shared data on each request
    @app.before_request
    def share_flash_messages():
        from flask import get_flashed_messages
        messages = []
        for category, message in get_flashed_messages(with_categories=True):
            messages.append({
                'type': category,
                'message': message
            })
        
        inertia.share({'flash': messages})