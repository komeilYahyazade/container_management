from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from .models import App, Container
from .serializers import AppSerializer, ContainerSerializer
import docker


class AppsAPIView(GenericAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.all()

    def get(self, request):
        apps = self.get_queryset()

        data = self.get_serializer(apps, many=True).data

        return Response(data={'apps': data},
                        status=status.HTTP_200_OK)


class AppAPIView(GenericAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        app = serializer.save()

        return Response(data={'name': app.name, 'image': app.image, 'id': app.id}, status=status.HTTP_200_OK)

    def get(self, request, app_id):
        app = get_object_or_404(App, id=app_id)

        data = self.get_serializer(app).data

        return Response(data={'app': data},
                        status=status.HTTP_200_OK)

    def put(self, request, app_id):
        app = get_object_or_404(App, id=app_id)
        updated_app = self.get_serializer(instance=app, data=request.data,
                                          partial=True)

        if updated_app.is_valid(raise_exception=True):
            updated_app.save(raise_exception=True)
        return Response(data={'details': 'app updated successfully'})

    def delete(self, request, app_id):
        self.get_queryset().filter(id=app_id).delete()
        return Response(data={'details': 'app deleted successfully'},
                        status=status.HTTP_200_OK)


class AppRunAPIView(GenericAPIView):

    def post(self, request, app_id):
        app = get_object_or_404(App, id=app_id)
        client = docker.from_env()
        container = client.containers.run(image=app.image, command=app.command, environment=app.envs, detach=True)
        Container.objects.create(app=app, image=app.image, command=app.command, envs=app.envs, name=app.name,
                                 container_id=container.id)

        return Response(
            data={'conaterner_id': container.id, 'app name': app.name, 'msg': "container started successfully"},
            status=status.HTTP_200_OK)


class AppHistoryAPIView(GenericAPIView):
    serializer_class = ContainerSerializer
    queryset = App.objects.all()

    def get(self, request, app_id):
        app = get_object_or_404(App, id=app_id)
        client = docker.from_env()
        for container in app.containers.all():
            container.state = client.api.inspect_container(container.container_id)['State']['Status']
            container.save()
        data = self.get_serializer(app.containers.all(), many=True).data

        return Response(data={'containers': data},
                        status=status.HTTP_200_OK)
