# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase

from app.views.views import download_file, download_receipt, export_csv


class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        user_password = "testing"
        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password=user_password)
        self.client.login(username=self.user.username, password=user_password)

        self.request_factory = RequestFactory()

        return super().setUp()

    def test_export_csv_get(self) -> None:
        request = self.request_factory.get(path="", data={"job": "test-job"})
        request.user = self.user

        response = export_csv(request=request)

        self.assertContains(response=response,
                            text="""<div class="progress">
                                <div class="bar" role="progressbar"></div>
                                </div>""",
                            status_code=200, html=True)

    def test_export_csv_post(self) -> None:
        request = self.request_factory.post(path="")
        request.user = self.user
        request.queryset = {}

        response = export_csv(request=request)

        self.assertEqual(first=response.status_code, second=302)

    def test_download_receipt_get(self) -> None:
        request = self.request_factory.get(path="", data={"job": "test-job"})
        request.user = self.user

        response = download_receipt(request=request)

        self.assertContains(response=response,
                            text="""<div class="progress">
                                <div class="bar" role="progressbar"></div>
                                </div>""",
                            status_code=200, html=True)

    def test_download_receipt_post(self) -> None:
        request = self.request_factory.post(path="")
        request.user = self.user
        request.queryset = {}

        response = download_receipt(request=request)

        self.assertEqual(first=response.status_code, second=302)

    def test_download_file_invalid_task(self) -> None:
        request = self.request_factory.get(
            path="", data={"task_id": "1", "task_name": "test"})
        request.user = self.user

        response = download_file(request=request)

        self.assertEqual(first=response.status_code, second=200)
