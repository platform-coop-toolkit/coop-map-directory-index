from datetime import date
from django.test import TestCase
from unittest.mock import patch
from .models import Organization
from datetime import timedelta


class YearsInOperationTestCase(TestCase):
    def setUp(self):
        Organization.objects.create(name='unknown', founded=None)
        Organization.objects.create(name='2020', founded='2020-01-01')
        Organization.objects.create(name='2010-07-01', founded='2010-07-01')

    def test_less_than_six_months(self):
        with patch('mdi.models.date') as mock_date:
            mock_date.today.return_value = date(2020, 6, 30)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            unknown = Organization.objects.get(name='unknown')
            self.assertEqual(unknown.years_operating(), 'Unknown')
            year_only = Organization.objects.get(name='2020')
            self.assertEqual(year_only.years_operating(), 0)
            year_month = Organization.objects.get(name='2010-07-01')
            self.assertEqual(year_month.years_operating(), 10)

    def test_more_than_six_months(self):
        with patch('mdi.models.date') as mock_date:
            mock_date.today.return_value = date(2020, 7, 1)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            unknown = Organization.objects.get(name='unknown')
            self.assertEqual(unknown.years_operating(), 'Unknown')
            year_only = Organization.objects.get(name='2020')
            self.assertEqual(year_only.years_operating(), 1)
            year_month = Organization.objects.get(name='2010-07-01')
            self.assertEqual(year_month.years_operating(), 10)
