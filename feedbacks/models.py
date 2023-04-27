from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Feedback(models.Model):
    text = models.TextField(max_length=500)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
