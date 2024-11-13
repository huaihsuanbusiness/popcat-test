from django.db import models

class Player(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    score = models.IntegerField(default=0)
    tap_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username or self.user_id
