from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Team, Player, Transfer, TransferHistory
from apps.account.serializers import UserSerializer
from utils import messages


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

    user = UserSerializer()


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name", "country")


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"

    team = TeamSerializer()


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"

    player = PlayerSerializer()


class TransferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ("player", "asking_price")

    def validate(self, attrs):
        if attrs["player"].team.user != self.context["request"].user:
            raise ValidationError(detail=messages.NOT_YOUR_PLAYER)

        if Transfer.objects.filter(player=attrs["player"], is_sold=False).exists():
            raise ValidationError(
                detail=messages.ACTIVE_TRANSFER_EXISTS_WITH_THIS_PLAYER
            )
        return attrs


class TransferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = (
            "asking_price",
            "player",
        )

    player = PlayerSerializer(read_only=True)


class TransferBuySerializer(serializers.Serializer):
    @transaction.atomic()
    def make_purchase(self, instance):
        player = instance.player
        current_team = player.team
        new_team = self.context["request"].user.team
        asking_price = instance.asking_price

        if asking_price > new_team.team_money:
            raise ValidationError(detail=messages.NOT_ENOUGH_MONEY)

        # updating player data
        player.team = new_team
        player.update_price(new_team.country)
        player.save()

        # updating teams' data
        current_team.team_money += asking_price
        current_team.save()
        new_team.team_money -= asking_price
        new_team.save()

        instance.is_sold = True
        instance.save()

        TransferHistory.objects.create(
            selling_team=current_team, buying_team=new_team, transfer=instance
        )
        return player


class TransferHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferHistory
        fields = "__all__"

    selling_team = TeamSerializer()
    buying_team = TeamSerializer()
    transfer = TransferSerializer()
