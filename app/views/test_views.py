# -*- coding: utf-8 -*-

from urllib.parse import parse_qs, urlparse

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase

from app.views.views import (
    download_file,
    download_receipt,
    export_csv,
    import_csv,
    poll_state,
)


class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        user_password = "testing"
        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password=user_password)
        self.client.login(username=self.user.username, password=user_password)

        self.request_factory = RequestFactory()

        return super().setUp()

    def test_import_csv_get(self) -> None:
        request = self.request_factory.get(path="", data={"job": "test-job"})
        request.user = self.user

        response = import_csv(request=request)

        self.assertContains(response=response,
                            text="""<div class="progress">
                                <div class="bar" role="progressbar"></div>
                                </div>""",
                            status_code=200, html=True)

    def test_import_csv_post(self) -> None:
        request = self.request_factory.post(path="")
        request.user = self.user
        request.queryset = {}

        response = import_csv(request=request)

        self.assertEqual(first=response.status_code, second=200)

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

    def test_download_receipt(self) -> None:
        download_receipt_request = self.request_factory.post(path="")
        download_receipt_request.user = self.user
        download_receipt_request.queryset = {}

        download_receipt_response = download_receipt(
            request=download_receipt_request)

        get_receipt_response = self.client.get(
            path=download_receipt_response.url)

        self.assertContains(response=get_receipt_response,
                            text="""<div class="progress">
                                <div class="bar" role="progressbar"></div>
                                </div>""",
                            status_code=200, html=True)

        location = download_receipt_response.get(header="Location")
        parsed_url = urlparse(url=location)
        query = parse_qs(qs=parsed_url.query)
        task_id = query["job"]
        poll_state_request = self.request_factory.post(
            path="", data={"task_id": task_id})
        poll_state_request.user = self.user

        poll_state_response = poll_state(request=poll_state_request)
        self.assertContains(
            response=poll_state_response,
            text="SUCCESS",
            status_code=200,
            html=True)

        download_file_request = self.request_factory.get(
            path="", data={"task_id": task_id})
        download_file_request.user = self.user

        download_file_response = download_file(request=download_file_request)
        content_type = download_file_response["Content-Type"]

        self.assertEqual(first=content_type, second="application/zip", msg=(
            "The content type of the receipt response was unexpected. "
            "Is Celery running with a results backend enabled?"))

    def test_poll_state(self) -> None:
        request = self.request_factory.post(
            path="", data={"task_id": "test-task-id"})
        request.user = self.user

        response = poll_state(request=request)

        print(response.content)
        self.assertEqual(first=response.status_code, second=200)
        self.assertJSONEqual(
            raw=response.content,
            expected_data={
                "state": "PENDING",
                "process_percent": 0,
                "status": 200},
        )
