import string
import random
from django.test import TestCase
from creo.models import Field, Config, Entries

class CompTestCase(TestCase):
    def setUp(self):

    	for i in range(100):
            Field(name='field%s' % i, value_type='S', default=random.choice(string.ascii_lowercase), user=0).save()

        c1 = Config(name='comp%s' % i, alias='c%s' % i, revision='A').save()
