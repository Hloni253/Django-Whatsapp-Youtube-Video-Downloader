from django.db import models

class YoutubeUrl(models.Model):
    verification_url = models.CharField(max_length=50)

    def str(self):
        return self.verification_url
