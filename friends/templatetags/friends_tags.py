from django import template
from friends.models import FriendRequest

register = template.Library()


@register.filter
def is_friend(user, current_user):
    if not user or not current_user:
        return False
    return FriendRequest.objects.filter(
        status='accepted'
    ).filter(
        from_user=current_user,
        to_user=user
    ).exists() or FriendRequest.objects.filter(
        status='accepted'
    ).filter(
        from_user=user,
        to_user=current_user
    ).exists()
