from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey


class Rule(models.Model):
    expression = models.TextField()
    reason = models.TextField()

    def __str__(self):
        return f"Rule {self.pk} {self.reason}"


class RuleSet(models.Model):
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    rules = models.ManyToManyField(Rule)

    def __str__(self):
        return f"RuleSet {self.pk}"
