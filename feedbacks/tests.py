from django.urls import reverse
from feedbacks.models import Feedback

def test_feedback_list_empty(client):
    # Проверка, что список обратной связи пуст, если в базе нет объектов Feedback
    url = reverse('feedbacks')
    response = client.get(url)
    # breakpoint()
    assert response.status_code == 200
    assert len(response.context['feedbacks']) == Feedback.objects.count()
