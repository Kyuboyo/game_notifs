from django.db import models
from common.models import BaseModel

class GamesModel(BaseModel):

    class StoreList(models.TextChoices):
        EPIC    = 'epic'
        STEAM   = 'steam'

    id = models.BigAutoField(primary_key=True)
    title = models.TextField(null=False)
    description = models.CharField(max_length=255, null=False)
    seller = models.TextField(null=False)
    store = models.TextField(choices=StoreList.choices, null=False)
    slug = models.TextField()

    def __str__(self):
        return f"{self.title}"


class ImagesModel(BaseModel):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(max_length=250)

    game = models.ForeignKey(GamesModel, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.id} {self.game.title}"

class CategoriesModel(BaseModel):
    id = models.BigAutoField(primary_key=True)
    category = models.TextField(null=False)

    game = models.ForeignKey(GamesModel, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.id} {self.game.title}"