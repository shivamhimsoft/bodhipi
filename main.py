from app import app
from inertia_flask import init_inertia

# Initialize Inertia
init_inertia(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
