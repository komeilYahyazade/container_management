from rest_framework import serializers

from .models import App, Container


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ('name', 'envs', 'image', 'command')

    def create(self, validated_data):
        app = super().create(validated_data=validated_data)
        return app


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ('name', 'envs', 'image', 'command', 'container_id', 'created_at', 'state')
