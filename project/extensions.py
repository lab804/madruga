from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# db
db = SQLAlchemy()

# migrate
migrate = Migrate()

marshmallow = Marshmallow()
