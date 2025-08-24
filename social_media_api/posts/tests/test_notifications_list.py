import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_notifications_on_like_and_comment(api_client, user_factory, post_factory, comment_factory):
    owner = user_factory()
    liker = user_factory()
    commenter = user_factory()
    post = post_factory(author=owner)

    # Like (creates notification via your LikeView)
    api_client.force_authenticate(user=liker)
    api_client.post(reverse('post-like-toggle', args=[post.id]))

    # Comment (creates notification via signal)
    comment = comment_factory(post=post, author=commenter)

    # Owner lists notifications
    api_client.force_authenticate(user=owner)
    resp = api_client.get(reverse('notifications-list'))
    assert resp.status_code == 200
    verbs = [n['verb'] for n in resp.data]
    assert "liked your post" in verbs
    assert "commented on your post" in verbs
