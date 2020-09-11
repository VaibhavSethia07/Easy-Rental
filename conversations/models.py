from django.db import models
from core import models as core_models

class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField("users.User", blank=True)
    

    def __str__(self):

        return self.created

class Message(core_models.TimeStampedModel):

    """ Message Model definition """

    message = models.TextField();
    user = models.ForeignKey("users.User", related_name="messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", related_name="messages", on_delete=models.CASCADE)
    send_date = models.DateField()  #Added
    send_time = models.TimeField()  #Added

    def __str__(self):

        return f"{self.user} says: {self.message}"