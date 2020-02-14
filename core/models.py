import os , uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from django.conf import settings


def image_filename(instance , filename):
	ext = filename.split('.')[-1]
	filename = f'{uuid.uuid4()}.{ext}'
	return os.path.join('upload/recipe/' , filename)


class UserManager(BaseUserManager):

	def create_user(self , email , password , **extra_fields):

		if not email:
			raise ValueError('User must have an email')

		email = self.normalize_email(email)
		user = self.model(email=email , **extra_fields)
		user.set_password(password)

		user.save(using=self._db)
		return user

	def create_superuser(self , email,password):

		user = self.create_user(email , password)

		user.is_superuser=True
		user.is_staff=True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser , PermissionsMixin):

	email = models.EmailField(max_length=255,unique=True)
	name = models.CharField(max_length=255)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'

class Tag(models.Model):

	name = models.CharField(max_length=255)
	user = models.ForeignKey(

		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE

		)

	def __str__(self):
		return self.name

class Ingredient(models.Model):

	name = models.CharField(max_length=255)
	user = models.ForeignKey(

		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE

		)

	def __str__(self):
		return self.name

class Recipe(models.Model):

	user = models.ForeignKey(

		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE

		)

	title = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=5 , decimal_places=2)
	time_minutes = models.IntegerField()
	ingredients = models.ManyToManyField('Ingredient')
	tags = models.ManyToManyField('Tag')
	image = models.ImageField(null=True , upload_to=image_filename)

	def __str__(self):
		return self.title



