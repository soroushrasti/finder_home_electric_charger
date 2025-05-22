from marshmallow import Schema, fields, validate, ValidationError, post_load


class UserSchema(Schema):
    UserID = fields.Integer(data_key="userId")
    Username = fields.Str(data_key="userName")

    def format_name(self, user):
        return f"{user.FirstName} {user.LastName}"


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserProfileSchema(Schema):
    UserID = fields.Integer(data_key="userId")
    Username = fields.Str(data_key="userName")

    
user_profile_schema = UserProfileSchema()

class UserCreationSchema(Schema):
    EditorEmail = fields.Email(required=True)

