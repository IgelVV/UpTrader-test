from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"Menu({self.pk}): {self.name}"


class MenuItem(models.Model):
    name = models.CharField(max_length=128)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"MenuItem({self.pk}): {self.name}"
