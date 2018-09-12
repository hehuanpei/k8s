from rest_framework import serializers
from cluster.models import Cluster


class ClusterSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Cluster
        fields = '__all__'