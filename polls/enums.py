from djchoices import ChoiceItem, DjangoChoices


class ChoiceTypeEnum(DjangoChoices):
    text = ChoiceItem("Ответ текстом", "Ответ текстом")
    one_point = ChoiceItem(
        "Ответ с выбором одного варианта", "Ответ с выбором одного варианта"
    )
    multiple_point = ChoiceItem(
        "Ответ с выбором нескольких вариантов", "Ответ с выбором нескольких вариантов"
    )
