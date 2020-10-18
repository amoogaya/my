import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Questions
from django.urls import reverse


# Create your tests here.
class QuestionsModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Questions(puplished_date=time)
        self.assertIs(future_question.was_puplished_recently(), False)

    def test_was_published_recently_with_older_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        older_question = Questions(puplished_date=time)
        self.assertIs(older_question.was_puplished_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Questions(puplished_date=time)
        self.assertIs(recent_question.was_puplished_recently(), True)


def add_new_question(question_text, days):
    time = timezone.now()+datetime.timedelta(days=days)
    return Questions.objects.create(question_text=question_text, puplished_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        add_new_question(question_text='past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Questions: past question>']

        )

    def test_future_question(self):
        add_new_question(question_text='future_text', days=50)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context['latest_questions'], []
        )

    def test_future_and_past_question(self):
        add_new_question(question_text='future_question', days=30)
        add_new_question(question_text='past_question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'], ['<Questions: past_question>']
        )

    def test_two_past_question(self):
        add_new_question(question_text='first_past_question', days=-30)
        add_new_question(question_text='second_past_question', days=-8)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Questions: first_past_question>', '<Questions: second_past_question>']
        )


class QuestionsDetailViewTest(TestCase):

    def test_future_question_detail(self):
        future_question = add_new_question(question_text='future question', days=60)
        url = reverse('polls:detailed', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_detail(self):
        past_question = add_new_question(question_text='past question', days=-8)
        print(past_question.id)
        url = reverse('polls:detailed', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
