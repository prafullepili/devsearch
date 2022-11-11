from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from yaml import serialize

from projects.models import Project,Review,Tag

from .serializers import ProjectSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'api/projects'},
        {'GET': 'api/projects/id'},
        {'POST': 'api/projects/id/vote'},

        {'{POST': 'api/users/token'},
        {'{POST': 'api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    serialize = ProjectSerializer(projects,many=True)
    return Response(serialize.data)


@api_view(['GET'])
def getProject(request,pk):
    projects = Project.objects.get(id=pk)
    serialize = ProjectSerializer(projects,many=False)
    return Response(serialize.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )
    # print("check for same project: ",str(review.project.owner),str(request.user))
    if str(review.project.owner)==str(request.user):
        return Response("You cannot vote your own project")
    review.value = data['value']
    review.save()
    project.getVoteCount

    serialize = ProjectSerializer(project,many=False)
    return Response(serialize.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']
    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)
    return Response('Tag was deleted!')