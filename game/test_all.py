from django.test import SimpleTestCase, TestCase, Client
from django.urls import  reverse, resolve
from game.views import home_view, games_query


class TestUrls(SimpleTestCase):
    def test_is_resolved(self):
        url = reverse('')
        self.asserteEquals(resolve(url).func, home_view)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.baseurl = reverse('')

    def test_home_get(self):
        response = self.client.get(self.baseurl)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

#
# class TestScrapper(SimpleTestCase):
#     def test_perhour(self):
#
#
#     def test_leaderboard(self):
#
#
#     def test_topplayers(self):
#
#
# class TestImport(SimpleTestCase):
#     def test_basedata(self):
#
#     def test_matches(self):
#
#
# class TestQueries(SimpleTestCase):
#     def test_relevantmaps(self):
#
#
#     def test_gamequeries(self):
