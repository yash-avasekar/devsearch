from projects.models import Project,Tag,Review
from users.models import Profile

from rest_framework import serializers


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


# Tag Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'



# Review Serializer
class ReviewSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    # review is child model so have to do this
    reviews = serializers.SerializerMethodField()
    
        
    class Meta:
        model = Project
        fields = '__all__'

    
    def get_reviews(self, instance):
        reviews = instance.review_set.all()
        serializer = ReviewSerialzer(reviews ,many=True)
        return serializer.data

