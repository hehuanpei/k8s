from __future__ import print_function
from pprint import pprint
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from kubernetes.client import Configuration, ApiClient, CoreV1Api
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from cluster.models import Cluster
from .serializers import ClusterSerializer
from kubernetes import client, config
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint

# /api/cluster/
class ClusterViewSet( viewsets.ModelViewSet ):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    # permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    # /api/cluster/list_service/
    @action( detail=True, methods=['get'] )
    def list_service(self, request, pk=None):
        cluster = get_object_or_404( Cluster, pk=pk )
        # pprint(v1_service_list)
        result = {}
        items = []
        config.load_kube_config()
        v1=client.CoreV1Api()
        try:
          ret=v1.list_service_for_all_namespaces(watch=False)
          for item in ret.items:
              items.append([item.metadata.namespace,item.metadata.name,item.spec.cluster_ip,str(item.spec.ports[0].port)+':'+str(item.spec.ports[0].node_port)+'/'+item.spec.ports[0].protocol])
          result['items'] = items
          return render( request, "table.html", {'result': result} )
        except ApiException as e:
          print("Exception when calling CoreV1Api->list_namespace: %s\n" % e)

        # /api/cluster/list_pod/
    @action( detail=True, methods=['get'] )
    def list_pod(self, request, pk=None):
        items=[]
        result={}
        config.load_kube_config()
        v1=client.CoreV1Api()
        try:
           ret=v1.list_pod_for_all_namespaces(watch=False)
           for item in ret.items:
                   items.append([item.metadata.namespace,item.metadata.name,item.status.host_ip,item.spec.node_name,item.status.phase])
                   #items.append([item.metadata.namespace,item.metadata.name,item.metadata.self_link])
                   result['items'] = items
                   pprint(result)
           return render( request, "table.html", {'result': result} )
        except ApiException as e:
           print("Exception when calling CoreV1Api->list_namespace: %s\n" % e)

