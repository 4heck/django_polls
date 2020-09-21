from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from polls.enums import ChoiceTypeEnum


class Poll(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Описание"
    )
    choice_type = models.CharField(
        choices=ChoiceTypeEnum.choices,
        default=ChoiceTypeEnum.text,
        max_length=100,
        verbose_name="Тип опроса",
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    end_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата окончания"
    )

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date <= self.pub_date:
            raise ValidationError(
                f"Дата оканчания не может быть раньше даты публикации"
            )

    class Meta:
        verbose_name = "опрос"
        verbose_name_plural = "опросы"


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll, related_name="choices", on_delete=models.CASCADE, verbose_name="Опрос"
    )
    choice_text = models.CharField(max_length=100, verbose_name="Выбор")

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = "вариант ответа"
        verbose_name_plural = "варианты ответа"


class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name="votes", on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("poll", "voted_by")
        verbose_name = "голос"
        verbose_name_plural = "голоса"
