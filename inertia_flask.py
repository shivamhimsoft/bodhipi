from flask_inertia import Inertia
import json
from flask import session, request, jsonify, render_template, make_response
from flask_login import current_user

# Initialize Inertia-Flask
inertia = Inertia()

# Fix for Inertia.js render method
def render_inertia(component_name, props=None, version=None):
    """Custom render method for Inertia"""
    if props is None:
        props = {}
    
    page_data = {
        'component': component_name,
        'props': props,
        'url': request.path,
        'version': version or '1'
    }
    
    if 'X-Inertia' in request.headers and request.headers['X-Inertia'] == 'true':
        response = make_response(jsonify(page_data))
        response.headers['X-Inertia'] = 'true'
        response.headers['Vary'] = 'Accept'
        return response
    
    return render_template('inertia.html', page=page_data)

# Add the custom render method to inertia
inertia.render = render_inertia

def init_inertia(app):
    """Initialize Inertia with the Flask app"""
    inertia.init_app(app)
    
    # Configure Inertia
    app.config["INERTIA_TEMPLATE"] = "inertia.html"
    
    # Add shared data for authentication
    @app.context_processor
    def inject_shared_data():
        auth_data = {}
        if current_user.is_authenticated:
            # Get unread message count
            unread_count = 0
            if hasattr(current_user, 'notifications'):
                unread_count = current_user.notifications.filter_by(read_status=False, type='message').count()
                
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
        
        # Combine all shared data
        return {**auth_data, **flash_data}