from api.models import User, Product
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users-detail')
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            try:
                user.save()
            except Exception as e:
                print("Exception: ")
                print(e)
            return user
        except Exception as e:
            print("Exception")
            print(e)
            raise ValueError('Error')

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['code',
                  'brands',
                  'keywords',
                  'categories_tags',
                  'countries',
                  'image_url',
                  'ingredients_text',
                  'user_id',
                  'sub_code']
