from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext
from .models import User

class UserAdmin(BaseUserAdmin):

	ordering=['id']
	list_display = ['id','email','name']

	fieldsets = (

		(None , {'fields':('email','password')}),
		(gettext('Personal Info') , {'fields':('name',)}),
		(gettext('Permissions'), {'fields':('is_active','is_staff','is_superuser')}),
		(gettext('Important dates') ,{'fields':('last_login',)})




		)

	add_fieldsets = (

		(None , {'classes':('wide',),'fields':('email','name','password1','password2')}),
		)


admin.site.register(User ,UserAdmin)