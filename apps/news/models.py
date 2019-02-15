from django.db import models

# Create your models here.
class Comment(models.Model):
    comment = models.CharField(max_length=100)
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("project.User", on_delete=models.CASCADE)
    news = models.ForeignKey("cms.News", on_delete=models.CASCADE,related_name="comments")

    class Meta:
        ordering = ["-pub_time"]

class Carousel(models.Model):
    position = models.IntegerField()
    image_url = models.URLField()
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]