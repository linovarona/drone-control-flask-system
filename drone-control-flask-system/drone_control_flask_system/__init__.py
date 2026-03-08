"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import drone_control_flask_system.views
