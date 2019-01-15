from app import app, db, search
from app.mixin import SearchableMixin
from flask_user import UserMixin, UserManager

# Define custom User Model with flask_user"s UserMixin
class Users(db.Model, UserMixin):
	__tablename__ = "users"
	__searchable__ = ["username",]

	id = db.Column(db.Integer, primary_key=True)

	# User authentication information
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False, server_default='')

	# User information
	first_name = db.Column(db.String(100), nullable=False, server_default='')
	last_name = db.Column(db.String(100), nullable=False, server_default='')
	active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")

	# Relationships
	roles = db.relationship('Roles', secondary='user_roles',
	backref = db.backref('users', lazy='dynamic'))

	# Define the relationship for author_id in terms and entrys models
	terms = db.relationship("terms", backref="author", lazy="dynamic")
	entrys = db.relationship("entrys", backref="author", lazy="dynamic")

# Define the Role data model
class Roles(db.Model):
	__tablename__ = "roles"

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True, nullable=False)

# Define the UserRoles data model
class UserRoles(db.Model):
	__tablename__ = "user_roles"

	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the Entry Model with custom SearchableMixin
# creation date/ time are only for full time view
class entrys(db.Model, SearchableMixin):
	__tablename__ = "entrys"
	__searchable__ = ["name", "content"]
	id = db.Column(db.Integer(), primary_key=True, unique=True)
	name = db.Column(db.String(150), server_default="")
	author_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
	creation_date = db.Column(db.String(20), server_default="")
	creation_time = db.Column(db.String(20), server_default="")
	content = db.Column(db.String(150), server_default="")

# Define the Term Model with custom SearchableMixin
# creation date/ time are only for full view
class terms(db.Model, SearchableMixin):
	__tablename__ = "terms"
	__searchable__ = ["name", "destination_day", "description"]
	id = db.Column(db.Integer(), primary_key=True, unique=True)
	name = db.Column(db.String(150))
	# author is only for traceability
	author_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
	creation_date = db.Column(db.String(20), server_default="")
	creation_time = db.Column(db.String(20), server_default="")
	destination_day = db.Column(db.String(20), server_default="")
	description = db.Column(db.String(150), server_default="")

# init of tabels
db.create_all()
