from django.db import models
from model_utils.models import TimeStampedModel


class Player(TimeStampedModel):
    POSITION_CHOICES = [
        ('G', 'guard'),
        ('F', 'forward'),
        ('C', 'center')
    ]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    uniform_number = models.IntegerField(null=True)
    injury = models.JSONField(null=True)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES, null=True)
    retire_year = models.IntegerField()


class Predict(TimeStampedModel):
    player_id = models.ForeignKey(Player, related_name="player_pred", on_delete=models.CASCADE,
                                  db_column="player_pred_id")
    predict_age = models.IntegerField()


class Image(TimeStampedModel):
    player_id = models.ForeignKey(Player, related_name="player_img", on_delete=models.CASCADE,
                                  db_column="player_img_id")
    url = models.ImageField(upload_to="nba_app", null=True)
