from collections import OrderedDict
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Goal(models.Model):
    """
    Represents a container that logically groups tasks together
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    tag = models.CharField(max_length=14, db_index=True)
    additional_info = JSONField(default=dict, blank=True)

    class Meta:
        unique_together = (("user", "tag"),)
        ordering = ['tag']

    def __str__(self):
        return "[{}] {}".format(self.tag, self.name)


class Task(models.Model):
    """
    Short, ideally less than one day activity.
    """
    TIME_CHOICES = (
        (1, '<1 Hour'),
        (2, '1-2 Hours'),
        (3, '2-4 Hours'),
        (4, '4-8 Hours'),
        (5, '8+ Hours')
    )
    ENERGY_CHOICES = (
        (1, 'No Energy at all'),
        (2, 'Little Energy'),
        (3, 'Moderate Energy'),
        (4, 'Heavy Energy'),
        (5, 'All-Consuming Energy')
    )
    FOCUS_CHOICES = (
        (1, 'No Attention at all'),
        (2, 'Little Attention'),
        (3, 'Concentration'),
        (4, 'Focused Concentration'),
        (5, 'Complete Concentration')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    additional_info = JSONField(default=dict, blank=True)
    time_difficulty = models.PositiveSmallIntegerField(
        choices=TIME_CHOICES,
        default=1
    )
    energy_difficulty = models.PositiveSmallIntegerField(
        choices=ENERGY_CHOICES,
        default=2
    )
    focus_difficulty = models.PositiveSmallIntegerField(
        choices=FOCUS_CHOICES,
        default=3
    )
    completed_info = JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    goals = models.ManyToManyField(Goal)

    class Meta:
        ordering = ['-id']

    @property
    def goal_ids(self):
        """Workaround property to initialize goals through DRF by ID
        """
        return [ goal.id for goal in self.goals.all() ]

    def __str__(self):
        return "{}".format(self.name)


class TaskAction(models.Model):
    """
    Represents current state of an activity
    (backlog, prioritized, in progress, paused, completed, discarded)
    """
    BACKLOG_CHOICE = 0
    PRIORITIZED_CHOICE = 1
    IN_PROGRESS_CHOICE = 2
    PAUSED_CHOICE = 3
    COMPLETED_CHOICE = 4
    DISCARDED_CHOICE = 5
    ACTION_CHOICES = (
        (BACKLOG_CHOICE, 'Backlog'),
        (PRIORITIZED_CHOICE, 'Prioritized'),
        (IN_PROGRESS_CHOICE, 'In Progress'),
        (PAUSED_CHOICE, 'Paused'),
        (COMPLETED_CHOICE, 'Completed'),
        (DISCARDED_CHOICE, 'Discarded')
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='actions')
    action = models.PositiveSmallIntegerField(
        choices=ACTION_CHOICES,
        default=1
    )
    initiated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-initiated']

    def clean(self):
        # Get the latest TaskAction
        last_action_obj = self.task.actions.first()
        if not last_action_obj:
            return
        current_action = self.action
        last_action = last_action_obj.action
        validate_last_and_current_action(last_action, current_action)

    def __str__(self):
        return "[{}] {}".format(self.get_action_display(), self.task)


def validate_last_and_current_action(last_action, current_action):
    if last_action == TaskAction.DISCARDED_CHOICE:
        raise ValidationError("Cannot update a task that has been discarded!")
    elif last_action == TaskAction.COMPLETED_CHOICE:
        raise ValidationError("Cannot update a task that has been completed!")
    elif last_action == TaskAction.PAUSED_CHOICE:
        if current_action not in [TaskAction.IN_PROGRESS_CHOICE, TaskAction.DISCARDED_CHOICE]:
            raise ValidationError("Paused tasks can only be changed to 'In Progress' or 'Discarded'!")
    elif last_action == TaskAction.IN_PROGRESS_CHOICE:
        if current_action not in [TaskAction.PAUSED_CHOICE, TaskAction.COMPLETED_CHOICE, TaskAction.DISCARDED_CHOICE]:
            raise ValidationError("In Progress tasks can only be changed to 'Paused', 'Completed', or 'Discarded'!")
    elif last_action == TaskAction.PRIORITIZED_CHOICE:
        if current_action not in [TaskAction.IN_PROGRESS_CHOICE, TaskAction.DISCARDED_CHOICE]:
            raise ValidationError("Prioritized tasks can only be changed to 'In Progress' or 'Discarded'!")
    elif last_action == TaskAction.BACKLOG_CHOICE:
        if current_action not in [TaskAction.PRIORITIZED_CHOICE, TaskAction.DISCARDED_CHOICE]:
            raise ValidationError("Backlog tasks can only be changed to 'Prioritized', or 'Discarded'!")


@receiver(models.signals.post_save, sender=Task)
def execute_after_task_save(sender, instance, created, *args, **kwargs):
    if created:
        TaskAction.objects.create(task=instance, action=TaskAction.BACKLOG_CHOICE)
