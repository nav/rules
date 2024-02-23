from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
import rule_engine
from api.rules import entities
from api.rules.models import RuleSet


class Rule(rule_engine.Rule):
    def __init__(self, text, reason=None, context=None):
        self.reason = reason
        super().__init__(text, context)

    def matches(self, thing):
        result = self.evaluate(thing)
        return result, self.reason


def get_conditions(content_object):
    context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
    today = timezone.now()

    content_type = ContentType.objects.get_for_model(content_object)
    rules = RuleSet.objects.get(
        content_type=content_type, object_id=content_object.pk
    ).rules.all()

    conditions = []
    for rule in rules:
        conditions.append(
            Rule(
                text=rule.expression.format(today=today),
                reason=rule.reason,
                context=context,
            )
        )

    return conditions


class RuleValidationMixin:
    def get_facts(self, attrs):
        request = self.context["request"]
        person = entities.Person(**request.person)

        product = None
        if "product" in attrs:
            _product = attrs["product"]
            product = entities.Product(
                sku=_product.sku,
                name=_product.name,
                available_until=_product.metadata.get("available_until"),
                available_in_states=_product.metadata.get("available_in_states"),
            )

        questionnaire = None
        if "questionnaire" in attrs:
            _ques = attrs["questionnaire"]
            questionnaire = entities.Questionnaire(
                are_you_pregnant=_ques["are_you_pregnant"]
            )

        return entities.Fact(
            person=person,
            product=product,
            questionnaire=questionnaire,
        )

    def get_ruleset_content_object(self, attrs):
        return attrs["product"]

    def validate(self, attrs):
        fact = self.get_facts(attrs)
        conditions = get_conditions(self.get_ruleset_content_object(attrs))

        reasons = []
        for condition in conditions:
            result, reason = condition.matches(fact)
            if not result:
                reasons.append(reason)

        if reasons:
            raise serializers.ValidationError(reasons)

        return attrs
