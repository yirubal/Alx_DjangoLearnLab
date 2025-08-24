import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_like_toggle_flow(api_client, user_factory, post_factory):
    user = user_factory()
    post = post_factory()
    api_client.force_authenticate(user=user)

    url = reverse('post-like-toggle', args=[post.id])

    # First like → 201 (created)
    r1 = api_client.post(url)
    assert r1.status_code == 201
    assert "liked the post" in r1.data["message"]

    # Second like (toggle) → 200 (unliked)
    r2 = api_client.post(url)
    assert r2.status_code == 200
    assert "unliked the post" in r2.data["message"]
