from bson import ObjectId
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .utils import users_collection


class MongoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get("user_id")
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                raise AuthenticationFailed("User not found")
            return user
        except Exception as e:
            raise AuthenticationFailed(str(e))
