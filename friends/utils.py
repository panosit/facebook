from django.db.models import Q
from .models import FriendRequest


def get_friend_ids(user):
    """Return a set of user IDs who are accepted friends of `user`."""
    accepted = FriendRequest.objects.filter(
        Q(from_user=user) | Q(to_user=user),
        status='accepted'
    )
    ids = set()
    for req in accepted:
        ids.add(req.to_user_id if req.from_user_id == user.id else req.from_user_id)
    return ids


def get_network_stats(user):
    """Return friend count and friends-of-friends count for `user`."""
    friend_ids = get_friend_ids(user)

    friends_of_friends = set()
    if friend_ids:
        accepted = FriendRequest.objects.filter(
            Q(from_user_id__in=friend_ids) | Q(to_user_id__in=friend_ids),
            status='accepted'
        )
        for req in accepted:
            friends_of_friends.add(req.from_user_id)
            friends_of_friends.add(req.to_user_id)

    friends_of_friends -= friend_ids
    friends_of_friends.discard(user.id)

    return {
        'friends_count': len(friend_ids),
        'friends_of_friends_count': len(friends_of_friends),
    }
