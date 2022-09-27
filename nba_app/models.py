from django.db import models
from model_utils.models import TimeStampedModel


class Player(TimeStampedModel):
    POSITION_CHOICES = [
        ('G', 'guard'),
        ('G-F', 'guard-forward'),
        ('F', 'forward'),
        ('F-G', 'forward-guard'),
        ('F-C', 'forward-center'),
        ('C', 'center'),
        ('C-F', 'center-forward')
    ]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    uniform_number = models.IntegerField(null=True)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, null=True)
    retire_year = models.IntegerField()
    season = models.IntegerField()
    injury_count = models.IntegerField()
    image = models.ImageField(upload_to="image/", default="")

    def __str__(self):
        return self.name


class Injury(TimeStampedModel):
    date = models.CharField(max_length=20)
    team = models.CharField(max_length=50)
    name = models.ForeignKey(Player, related_name="player_injury", on_delete=models.CASCADE,
                             db_column="player_injury_id")
    injury_details = models.TextField()


class Predict(TimeStampedModel):
    player_id = models.ForeignKey(Player, related_name="player_pred", on_delete=models.CASCADE,
                                  db_column="player_pred_id")
    predict_age = models.IntegerField()


class Image(TimeStampedModel):
    player_id = models.ForeignKey(Player, related_name="player_img", on_delete=models.CASCADE,
                                  db_column="player_img_id")
    url = models.ImageField(upload_to="nba_app", null=True)
