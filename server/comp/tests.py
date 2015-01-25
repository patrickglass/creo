from django.test import TestCase
from comp.models import Comp


class CompTestCase(TestCase):
    def setUp(self):
        for i in range(100):
            Comp(name='comp%s' % i, alias='c%s' % i, revision='A').save()
