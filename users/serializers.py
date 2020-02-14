from rest_framework import serializers
from core.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy


class CreateUserSerializer(serializers.ModelSerializer):

	class Meta:

		model = User
		fields = ('email','name','password')
		extra_kwargs = {'password':{'write_only':True}}

	def create(self , validated_data):

		user = User.objects.create_user(**validated_data)
		return user

	def update(self , instance , validated_data):

		password = validated_data.pop('password',None)
		user = super().update(instance , validated_data)

		if password:
			user.set_password(password)
			user.save()

		return user
		

class UserLoginSerializer(serializers.Serializer):

	email = serializers.CharField()
	password = serializers.CharField(

		style={'input_type':'password'},
		trim_whitespace=False
		)

	def validate(self , attrs):

		email = attrs.get('email')
		password = attrs.get('password')

		user = authenticate(

			request = self.context.get('request'),
			username=email,
			password=password
			)

		if not user:

			msg = ugettext_lazy('Unable to authenticate with provided credentials')
			raise serializers.ValidationError(msg , code="authentication")

		attrs['user']=user
		return attrs
