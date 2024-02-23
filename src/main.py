import timeit
import datetime
import rule_engine
import entities
import rules


def run():
    context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
    today = datetime.datetime.now()

    conditions = [
        rules.Rule(
            "person.age >= 18",
            "Person's age must be 18 or older.",
            context=context,
        ),
        rules.Rule(
            "person.age < 65",
            "Person's age must be 64 and younger.",
            context=context,
        ),
        rules.Rule(
            "person.sex_at_birth == 'female'",
            "Person must be female.",
            context=context,
        ),
        rules.Rule(
            "questionnaire.are_you_pregnant == false",
            "Person must not be pregnant.",
            context=context,
        ),
        rules.Rule(
            f"product.available_until <= d'{today}'",
            "Product is no longer available to order.",
            context=context,
        ),
        rules.Rule(
            f"person.address_state in product.available_in_states",
            "Product is not available in your state.",
            context=context,
        ),
    ]

    fact = entities.Fact(
        person=entities.Person(
            organization=entities.Organization(name="ixlayer"),
            age=11,
            sex_at_birth="male",
            address_state="CA",
            address_country="US",
        ),
        questionnaire=entities.Questionnaire(are_you_pregnant=False),
        product=entities.Product(
            name="Some Product",
            sku="product-a",
            available_until=datetime.datetime(year=2024, month=2, day=20),
            available_in_states=["NY", "CA"],
        ),
    )

    reasons = []
    for condition in conditions:
        result, reason = condition.matches(fact)
        if not result:
            reasons.append(reason)

    return reasons


if __name__ == "__main__":
    print(run())
