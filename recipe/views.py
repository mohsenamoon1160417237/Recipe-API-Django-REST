from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import viewsets , mixins , status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers
from core.models import Tag,Ingredient,Recipe


class BaseRecipeViewSet(viewsets.GenericViewSet , mixins.ListModelMixin , mixins.CreateModelMixin):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):

		assigned_only = bool(self.request.query_params.get('assigned_only'))
		queryset = self.queryset
		if assigned_only:
			queryset = queryset.filter(recipe__isnull=False)

		return queryset.filter(user=self.request.user).order_by('-name')

	def perform_create(self , serializer):

		serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeViewSet):


	serializer_class = serializers.TagSerializer
	queryset = Tag.objects.all()



class IngredientViewSet(BaseRecipeViewSet):

	serializer_class = serializers.IngredientSerializer
	queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):

	serializer_class = serializers.RecipeSerializer
	queryset = Recipe.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def _params_to_int(self , qs):

		return [int(str_id) for str_id in qs.split(',')]

	def get_queryest(self):

		tags = self.request.query_params.get('tags')
		ingredients = self.request.query_params.get('ingredients')
		queryset = self.queryset
		if tags:
			tag_ids = self._params_to_int(tags)
			queryst = queryset.filter(tags__id__in=tag_ids)
		if ingredients:
			ingredient_ids = self._params_to_int(ingredients)
			queryest = queryset.filter(ingredients__id__in=ingredient_ids)


		return queryset.filter(user=self.requet.user)

	def perform_create(self , serializer):

		serializer.save(user=self.request.user)

	def get_serializer_class(self):

		if self.action == 'retrieve':
			return serializers.RecipeDetailSerializer

		if self.action =='upload_image':
			return serializers.RecipeImageSerializer

		return self.serializer_class

	@action(methods=['POST'] , detail=True , url_path='upload-image')
	def upload_image(self , request , pk=None):

		recipe= self.get_object()
		serializer = self.get_serializer(

			recipe,
			data=request.data
			)
		if serializer.is_valid():
			serializer.save()
			return Response(
				serializer.data,
				status=status.HTTP_200_OK

				)

		return Response(

			serializer.errors,
			status=status.HTTP_404_BAD_REQUEST

			)


