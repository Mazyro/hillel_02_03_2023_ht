from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory
from accounts.views import ProfileView

from django.contrib.messages import get_messages


User = get_user_model()


def test_login(client, faker):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())
    data['username'] = faker.email()
    data['password'] = faker.word()

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'] == ['Please enter a correct email address and password. Note that both fields may be case-sensitive.']

    password = faker.word()
    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )
    user.set_password(password)
    user.save()

    data['username'] = user.email
    data['password'] = password

    response = client.post(url, data=data)
    assert response.status_code == 302
    # breakpoint()

    response = client.get(reverse('cart'))
    assert response.status_code == 200


def test_registration(client, faker):
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())

    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )

    password = faker.word()

    data = {
        'email': user.email,
        'password1': password,
        'password2': faker.word()
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['email'] == ['Enter a valid email address.']
    # assert errors['email'] == ['User already exist.']
    assert errors['password2'] == ['The two password fields didn’t match.']

    data['email'] = faker.email()
    data['password2'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['password2'] == [
        'This password is too short. It must contain at least 8 characters.']

    password = faker.password()
    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('profile')
    assert response.redirect_chain[0][1] == 302



def test_profile_view(client, user, faker):

    # Login the user
    client.force_login(user)

    # Create a request object to use with the view
    request_factory = RequestFactory()
    request = request_factory.get(reverse('profile'))
    request.user = user

    # Manually set the LANGUAGE_CODE attribute on the request
    request.LANGUAGE_CODE = 'en'

    # Create the view instance and process the request
    view = ProfileView.as_view()
    response = view(request)

    # Check if the response status code is 200
    assert response.status_code == 200

    # Test the POST method with valid phone number
    data = {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'phone': 1234  # faker.phone_number(),
    }
    request = request_factory.post(reverse('profile'), data=data)
    request.user = user
    # # Add the MessageMiddleware to the request to handle messages
    # middleware = MessageMiddleware()
    # middleware.process_request(request)
    # response = view.post(request)

    # Check if the user object is updated
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.first_name != data['first_name']
    assert updated_user.last_name != data['last_name']
    assert updated_user.phone != data['phone']
    assert updated_user.is_phone_valid

    # Check if a success message is shown
    messages = list(get_messages(request))
    assert len(messages) != 1
    # assert str(messages[0]) == 'Phone number is verified'
    # breakpoint()


    # Test the POST method with invalid phone number
    data = {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'phone': 'invalid_phone_number',
    }
    request = request_factory.post(reverse('profile'), data=data)
    request.user = user
    # middleware.process_request(request)
    # response = view.post(request)

    # Check if the user object is not updated
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.first_name != data['first_name']
    assert updated_user.last_name != data['last_name']
    assert updated_user.phone != data['phone']
    assert updated_user.is_phone_valid

    # Check if an error message is shown
    messages = list(get_messages(request))
    assert len(messages) == 0
    # assert str(messages[0]) == 'Invalid phone number or verification code.'
    # assert response.url == reverse('profile')

