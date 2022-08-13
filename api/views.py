# To work with views based on function
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializes import ProjectSerializer
from projects.models import Project, Review, Tag


# All urls which we have in side our api
# And types of the methods which we can send here
@api_view(['GET'])  # 'PUT', 'DELETE'
def getRoutes(request):

    routes = [
        {'GET': 'api/projects'},
        {'GET': 'api/projects/id'},
        {'POST': 'api/projects/id/vote'},

        # Get access to api
        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},

    ]

    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    # Convert our queryset to JSON data
    # Must be specified many = True | False
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):

    project = Project.objects.get(id=pk)

    # Convert our queryset to JSON data
    # Must be specified many = False because we get only single project
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    # data['value'] from body request
    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response("Tag was deleted!")
