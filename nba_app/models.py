from django.db import models
from model_utils.models import TimeStampedModel


class Player(TimeStampedModel):
    name = models.CharField(max_length=100)
    uniform_number = models.IntegerField()

class Predict(TimeStampedModel):
    pass


class Image(TimeStampedModel):
    player_id = models.ForeignKey(Player, related_name="player", on_delete=models.CASCADE, db_column="player_id")
    url = models.ImageField(upload_to="nba_app", null=True)

