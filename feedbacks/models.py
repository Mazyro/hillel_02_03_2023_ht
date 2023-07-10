from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django_lifecycle import LifecycleModelMixin, hook, \
    AFTER_CREATE, AFTER_UPDATE
from django.core.cache import cache
from project.model_choices import FeedbackCacheKeys

User = get_user_model()


class Feedback(LifecycleModelMixin, models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    text = models.TextField(
        max_length=1024,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.user}  -- Rating {self.rating} -- Text {self.text}"

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_signal(self):
        cache.delete(FeedbackCacheKeys.FEEDBACKS)
