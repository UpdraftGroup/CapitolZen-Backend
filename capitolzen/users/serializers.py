from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework.validators import UniqueValidator
from pprint import pprint
from .models import User


class UserSerializer(serializers.ModelSerializer):
    organizations = ResourceRelatedField(
        many=True,
        read_only=True,
        source='organizations_organization'
    )

    username = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'user_is_staff', 'user_is_admin', 'organizations')
        # this currently breaks users with: TypeError: The `exclude` option must be a list or tuple. Got str.
        # exclude = 'password'
        read_only_fields = ('id', 'user_is_staff', 'user_is_admin', 'organizations')
        lookup_field = 'username'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
