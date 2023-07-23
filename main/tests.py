from django.urls import reverse


# Тест для проверки успешного отображения страницы MainView:
def test_main_view(client):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200
    assert 'main/index.html' in response.template_name


# Тест для проверки отображения страницы ContactView и успешной отправки формы:
def test_contact_view(client, faker):
    url = reverse('contacts')
    data = {
        'email': faker.email(),
        'text': faker.text(),
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert 'main/index.html' in response.template_name
