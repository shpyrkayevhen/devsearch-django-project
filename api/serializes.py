# Serializers data before we will return it. We
# have the Python objects and convert them to JSON
from rest_framework import serializers
# Also import related tables with Project and
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


# Serialize all obj our model to JSON data
class ProjectSerializer(serializers.ModelSerializer):
    # As a Project table has the atributes (related fields) owner & tags
    # We also want to get information about owner field and tags
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    # Adds this attribute just to this Serializer class
    # We want to see all reviews for particular obj
    # as we have related field from Review to Project
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    # If we want to add method to our ProjectSerializer need start get_
    # self: class ProjectSerializer, obj: model Project.

    def get_reviews(self, obj):
        # review_set: because we have related field from Review to Project
        # Many - to - Many relationship. Get all reviews for this project
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
