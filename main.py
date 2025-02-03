from flask import Flask, Blueprint
import config
import routes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Enable debug mode based on configuration
app.debug = config.DEBUG

# Register blueprints dynamically
for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(blueprint, url_prefix=blueprint.url_prefix)

if __name__ == "__main__":
    print(f"Application running on http://{config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT)
