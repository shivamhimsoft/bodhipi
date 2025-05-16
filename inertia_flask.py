from flask import request, render_template, jsonify, make_response, session, get_flashed_messages
from flask_login import current_user
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SimpleInertia:
    """A simple Inertia implementation for Flask"""
    
    def __init__(self):
        self.shared_props = {}
        self.version = datetime.now().strftime("%Y%m%d%H%M%S")
    
    def share(self, data):
        """Share data across all Inertia responses"""
        if isinstance(data, dict):
            self.shared_props.update(data)
        else:
            logger.warning("Invalid data type provided to inertia.share(), expected dict")
    
    def render(self, component_name, props=None, version=None):
        """Render an Inertia-powered page with the specified React component"""
        if props is None:
            props = {}
        
        # Use provided version or default
        version = version or self.version
        
        # Include authentication info
        auth_data = None
        if current_user.is_authenticated:
            # Get unread message count if available
            unread_count = 0
            if hasattr(current_user, 'notifications'):
                try:
                    unread_count = current_user.notifications.filter_by(read_status=False, type='message').count()
                except Exception as e:
                    logger.warning(f"Error getting unread count: {str(e)}")
                    unread_count = 0
            
            # Create authentication data object for the frontend
            auth_data = {
                'id': current_user.id,
                'email': current_user.email,
                'user_type': current_user.user_type,
                'unread_count': unread_count
            }
        
        # Get flash messages
        messages = []
        for category, message in get_flashed_messages(with_categories=True):
            messages.append({
                'type': category,
                'message': message
            })
        
        # Merge all props with shared data
        all_props = {
            **self.shared_props,
            **props,
            'auth': auth_data,
            'flash': messages,
            'csrf_token': session.get('csrf_token', '')
        }
        
        # Create the Inertia page object
        page_data = {
            'component': component_name,
            'props': all_props,
            'url': request.path,
            'version': version
        }
        
        # Log page data for debugging (remove in production)
        logger.debug(f"Rendering {component_name} with props: {json.dumps(all_props, default=str)[:200]}...")
        
        # Handle Inertia XHR requests
        if 'X-Inertia' in request.headers and request.headers['X-Inertia'] == 'true':
            response = make_response(jsonify(page_data))
            response.headers['X-Inertia'] = 'true'
            response.headers['Vary'] = 'Accept'
            return response
        
        # Return standard HTML response with the Inertia page data
        return render_template('inertia.html', page=page_data)

# Create global instance
inertia = SimpleInertia()

def init_inertia(app):
    """Initialize Inertia with the Flask app"""
    # Configure Inertia
    app.config["INERTIA_TEMPLATE"] = "inertia.html"
    
    # Generate CSRF token for forms if needed
    @app.before_request
    def generate_csrf_token():
        if 'csrf_token' not in session:
            import secrets
            session['csrf_token'] = secrets.token_hex(16)
    
    # Add Jinja template function for CSRF token
    @app.template_global()
    def csrf_token():
        if 'csrf_token' not in session:
            import secrets
            session['csrf_token'] = secrets.token_hex(16)
        return session['csrf_token']