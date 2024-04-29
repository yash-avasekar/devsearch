from rest_framework import status

from . import serializers
from projects.models import Project,Review

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



# get projects 
@api_view(['GET'])
def getProjects(request):
    
    projects = Project.objects.all()
    # seralizer multiple projects
    serializer = serializers.ProjectSerializer(projects ,many=True)

    return Response(serializer.data ,status=status.HTTP_200_OK)


# get single project 
@api_view(['GET'])
def getProject(request ,pk):
    projects = Project.objects.get(id = pk)
    # seralizer multiple projects
    serializer = serializers.ProjectSerializer(projects ,many=False)

    return Response(serializer.data ,status=status.HTTP_200_OK)


# project vote 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request ,pk):
    user = request.user.profile
    project = Project.objects.get(id = pk)
    serializer = serializers.ProjectSerializer(project ,many=False)

    data = request.data # get data

    # get view to save data
    review ,created = Review.objects.get_or_create(
        owner = user,
        project = project
    )

    review.value = data['value']
    review.save()
    project.getVoteCount

    return Response('Your vote was added' ,status=status.HTTP_201_CREATED)