import random
import names


from django.contrib.auth import get_user_model
from django_countries import countries
from celery import shared_task

from apps.core.models import Team, Player
from utils import email as email_tool, messages, constants


User = get_user_model()


@shared_task()
def forgot_password_task(email, password):
    subject = messages.FORGOT_EMAIL_SUBJECT
    body = (
        "Hi, your new password for fantasy game: {}. "
        "Please, change your password after first login".format(password)
    )
    email_tool.send_email(email, subject, body)


@shared_task()
def create_team_for_user(user_id):
    user = User.objects.get(id=user_id)
    team_country = random.choice(list(countries))[1]
    team = Team.objects.create(
        user=user, name=names.get_full_name(), country=team_country
    )

    create_players(constants.DEFAULT_DEFENDER_AMOUNT, constants.DEFENDER, team)
    create_players(constants.DEFAULT_MIDFIELDER_AMOUNT, constants.MIDFIELDER, team)
    create_players(constants.DEFAULT_GOALKEEPER_AMOUNT, constants.GOALKEEPER, team)
    create_players(constants.DEFAULT_ATTACKER_AMOUNT, constants.ATTACKER, team)


def create_players(amount, position, team):
    for i in range(amount):
        player_country = random.choice(list(countries))[1]
        Player.objects.create(
            first_name=names.get_first_name(),
            last_name=names.get_last_name(),
            country=player_country,
            age=random.randint(
                constants.MINIMUM_AGE_FOR_PLAYER, constants.MAXIMUM_AGE_FOR_PLAYER
            ),
            position=position,
            team=team,
        )
