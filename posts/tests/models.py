import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from posts.models import Post


class PostTestCase(TestCase):
    fixtures = ['posts_views_testdata.json']

    def setUp(self):
        super(PostTestCase, self).setUp()
        self.post_1 = Post.objects.get(pk=1)
        self.post_2 = Post.objects.get(pk=2)

    def test_published_manager(self):
        # Checking if publish manager is giving us the right number of posts
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(Post.published.all().count(), 1)

        self.post_1.published_date = datetime.datetime.now()
        self.post_1.save()

        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(Post.published.all().count(), 2)

    def test_publish_method(self):
        # Checking if publish method is working correctly
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(Post.published.all().count(), 1)

        self.post_1.publish()

        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(Post.published.all().count(), 2)

    def test_unpublish_method(self):
        # Checking if unpublish method is working correctly
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(Post.published.all().count(), 1)

        self.post_2.unpublish()

        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(Post.published.all().count(), 0)

    def test_no_future_posts(self):
        # Checking if future-dates Post are showing in published manager
        post = Post.objects.create(
            author=User.objects.get(id=1),
            title="Is potato salad any good?",
            content="Not",
            published_date=datetime.datetime.now() + datetime.timedelta(days=1)
        )

        self.assertEqual(Post.objects.all().count(), 3)
        self.assertEqual(Post.published.all().count(), 1)
