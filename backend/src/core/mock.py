from src.auth.models import User


def get_mock_user(x: int = 1) -> User:

    mocked_users = {
        1: User(id=1, username='MoonPie', password='test123'),
        2: User(id=2, username='Billie Jean King', password='test123')
    }

    return mocked_users[x]