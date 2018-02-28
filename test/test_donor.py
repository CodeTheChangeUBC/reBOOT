
from app import models
from app.models import Donation
from app.models import Donor
from django.db import IntegrityError

import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:
    pytestmark = pytest.mark.django_db


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()


def test_donor_with_complete_fields():
    test_donor = Donor(donor_name='Tesla', email='NickT@gmail.com', want_receipt=True,
                       telephone_number='604-123-5678', mobile_number='604-123-5678',
                       address_line='Mars street', city='Tokyo',
                       province='Japan', postal_code='123123', verified=True)
    test_donor.save()

    response = Donor.objects.get(donor_name='Tesla')
    assert response.donor_name == 'Tesla'
    assert response.email == 'NickT@gmail.com'
    assert response.want_receipt == True
    assert response.telephone_number == '604-123-5678'
    assert response.mobile_number == '604-123-5678'
    assert response.address_line == 'Mars street'
    assert response.city == 'Tokyo'
    assert response.province == 'Japan'
    assert response.postal_code == '123123'
    assert response.verified == True


def test_donor_bad_phonenumber():
    # DOES NOT THROW ANYTHING.
    test_donor = Donor(donor_name='Zavala',
                       telephone_number='111122223333123', want_receipt=False)
    test_donor.save()


def test_donor_null_for_want_receipt():
    with pytest.raises(IntegrityError):
        test_donor = Donor(donor_name='Tohru', telephone_number='123-333-3333')
        test_donor.save()


def test_invalid_postal_code():
    test_donor = Donor(donor_name='Kobayashi',
                       postal_code='12345678123afasdf', want_receipt=False)
    test_donor.save()
    response = Donor.objects.get(donor_name='Kobayashi')
    assert len(response.postal_code) == 7
