from clients.users.test_client import get_users_client, CreateUserRequestDict
from clients.private_http_builder import AuthenticationUserDict

create_users_request = CreateUserRequestDict(
    email="1@1.com",
    password="123456",
    lastName="qwerty",
    firstName="qwerty",
    middleName="qwerty",
)

authentication_user = AuthenticationUserDict(
    email=create_users_request['email'],
    password=create_users_request['password']
)

users_client = get_users_client(authentication_user)


create_user_response = users_client.create_user(create_users_request)
print('Create user data:', create_user_response)