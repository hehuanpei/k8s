from django.db import models

class Cluster(models.Model):
    name = models.TextField()
    api = models.TextField()
    token = models.TextField()

    class Meta :
        db_table = "cluster"

    def __str__(self):
        return self.name

