from api.models import Goal, Task, TaskAction, validate_last_and_current_action
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name')


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'user', 'name', 'tag', 'additional_info')

    def create(self, validated_data):
        request = self.context.get("request")
        request_user = request.user
        validated_data['user'] = request_user
        return super(GoalSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        request_user = request.user
        validated_data['user'] = request_user
        return super(GoalSerializer, self).update(instance, validated_data)


class TaskActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAction
        fields = ('id', 'task', 'action', 'initiated')

    def validate(self, attrs):
        # Get the user, ensure tasks match
        request = self.context.get("request")
        request_user = request.user
        if attrs.get('task').user != request_user:
            raise ValidationError('Request user mismatch for task!')
        # Get the latest TaskAction
        last_action_obj = attrs.get('task').actions.first()
        if last_action_obj:
            current_action = attrs.get('action')
            last_action = last_action_obj.action
            validate_last_and_current_action(last_action, current_action)
        return attrs


class TaskSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    actions = TaskActionSerializer(many=True, read_only=True)
    # When passed a list of Goal IDs in goal_ids, will initialize the Task with those IDs.
    goal_ids = serializers.ListField(child=serializers.IntegerField())

    def initialize_goals(self, obj):
        obj.goals
        return False

    class Meta:
        model = Task
        fields = ('id', 'user', 'name', 'additional_info', 'time_difficulty',
                  'energy_difficulty', 'focus_difficulty', 'completed_info',
                  'created', 'updated', 'goals', 'actions', 'goal_ids')

    def create(self, validated_data):
        request = self.context.get("request")
        request_user = request.user
        goal_ids = set(validated_data.pop('goal_ids'))
        validated_data['user'] = request_user

        task = Task.objects.create(**validated_data)
        for goal_id in goal_ids:
            try:
                goal = Goal.objects.get(pk=goal_id)
                if goal.user == task.user:
                    task.goals.add(goal)
            except Goal.DoesNotExist:
                pass
        return task

    def update(self, instance, validated_data):
        request = self.context.get("request")
        request_user = request.user
        # Get the user, ensure tasks match
        if instance.user != request_user:
            raise ValidationError('Request user mismatch for task!')

        validated_data['user'] = request_user
        goal_ids = set(validated_data.pop('goal_ids'))
        task = super(TaskSerializer, self).update(instance, validated_data)

        original_goal_ids = set(instance.goal_ids)
        goal_ids_to_add = goal_ids - original_goal_ids
        for goal_id in goal_ids_to_add:
            try:
                goal = Goal.objects.get(pk=goal_id)
                if goal.user == task.user:
                    task.goals.add(goal)
            except Goal.DoesNotExist:
                pass
        goal_ids_to_remove = original_goal_ids - goal_ids
        for goal_id in goal_ids_to_remove:
            try:
                goal = Goal.objects.get(pk=goal_id)
                task.goals.remove(goal)
            except Goal.DoesNotExist:
                pass
        return task
