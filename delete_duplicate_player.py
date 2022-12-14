import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nba_predict_django.settings'
import django

django.setup()
from nba_app.models import Player
from django.db.models import Count

delete_pk = []
player_obj = Player.objects.values('name').annotate(cnt=Count('id')).filter(cnt__gte=2)
for i in player_obj:
    name = i['name']
    obj = Player.objects.filter(name=name).order_by("retire_year")[0]
    obj.delete()

