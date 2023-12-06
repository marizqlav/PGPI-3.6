from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.

from django.db import models
from users.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5,validators=[MaxValueValidator(5)])

    def __str__(self):
        return self.title