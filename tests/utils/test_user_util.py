from types import SimpleNamespace

from tests.utils import user_util


def test_user_util_get_test_user_reuses_cached_non_random(monkeypatch):
    monkeypatch.setattr(
        user_util,
        "settings",
        SimpleNamespace(
            test_user_email="test_user@example.com",
            test_user_password="password",
        ),
    )
    monkeypatch.setattr(user_util, "test_user", None)

    auth_call_count = {"count": 0}

    monkeypatch.setattr(
        user_util,
        "supabase_get_user_from_email",
        lambda email: {"id": "user-1", "auth_user_id": "auth-1"},
    )
    monkeypatch.setattr(
        user_util,
        "supabase_register_user",
        lambda email, password: None,
    )

    def fake_auth(email, password):
        auth_call_count["count"] += 1
        return {"access_token": "token-1"}, {"id": "user-1", "auth_user_id": "auth-1"}

    monkeypatch.setattr(user_util, "supabase_auth_with_password", fake_auth)

    first_session, first_user = user_util.user_util_get_test_user()
    second_session, second_user = user_util.user_util_get_test_user()

    assert first_session == second_session
    assert first_user == second_user
    assert auth_call_count["count"] == 1


def test_user_util_get_test_user_random_does_not_override_cached(monkeypatch):
    monkeypatch.setattr(
        user_util,
        "test_user",
        (
            {"access_token": "cached"},
            {"id": "cached", "auth_user_id": "cached-auth"},
        ),
    )

    monkeypatch.setattr(
        user_util,
        "supabase_get_user_from_email",
        lambda email: {"id": "random-user", "auth_user_id": "random-auth"},
    )
    monkeypatch.setattr(
        user_util,
        "supabase_register_user",
        lambda email, password: None,
    )
    monkeypatch.setattr(
        user_util,
        "supabase_auth_with_password",
        lambda email, password: (
            {"access_token": "random-token"},
            {"id": "random-user", "auth_user_id": "random-auth"},
        ),
    )

    random_session, random_user = user_util.user_util_get_test_user(random=True)

    assert random_session["access_token"] == "random-token"
    assert random_user["id"] == "random-user"
    assert user_util.test_user == (
        {"access_token": "cached"},
        {"id": "cached", "auth_user_id": "cached-auth"},
    )
