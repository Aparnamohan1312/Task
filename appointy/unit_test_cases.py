import     itertools
 	import tempfile
	from unittest import mock
	

	from django.contrib.auth.models import User
	from django.core import mail
	from django.http import HttpResponse
	from django.test import (
	    Client, RequestFactory, SimpleTestCase, TestCase, override_settings,
	)
	from django.urls import reverse_lazy
	

	from .views import TwoArgException, get_view, post_view, trace_view
	

	

	@override_settings(ROOT_URLCONF='test_client.urls')
	class ClientTest(TestCase):
	

	    @classmethod
	    def setUpTestData(cls):
	        cls.u1 = User.objects.create_user(username='testclient', password='password')
	        cls.u2 = User.objects.create_user(username='inactive', password='password', is_active=False)
	

	    def test_get_view(self):
	        "GET a view"
	        # The data is ignored, but let's check it doesn't crash the system
	        # anyway.
	        data = {'var': '\xf2'}
	        response = self.client.get('/get_view/', data)
	

	        # Check some response details
	        self.assertContains(response, 'This is a test')
	        self.assertEqual(response.context['var'], '\xf2')
	        self.assertEqual(response.templates[0].name, 'GET Template')
	

	    def test_query_string_encoding(self):
	        # WSGI requires latin-1 encoded strings.
	        response = self.client.get('/get_view/?var=1\ufffd')
	        self.assertEqual(response.context['var'], '1\ufffd')
	

	    def test_get_data_none(self):
	        msg = (
	            "Cannot encode None for key 'value' in a query string. Did you "
	            "mean to pass an empty string or omit the value?"
	        )
	        with self.assertRaisesMessage(TypeError, msg):
	            self.client.get('/get_view/', {'value': None})
	

	    def test_get_post_view(self):
	        "GET a view that normally expects POSTs"
	        response = self.client.get('/post_view/', {})
	

	        # Check some response details
	        self.assertEqual(response.status_code, 200)
	        self.assertEqual(response.templates[0].name, 'Empty GET Template')
	        self.assertTemplateUsed(response, 'Empty GET Template')
	        self.assertTemplateNotUsed(response, 'Empty POST Template')
	

	    def test_empty_post(self):
	        "POST an empty dictionary to a view"
	        response = self.client.post('/post_view/', {})
	

	        # Check some response details
	        self.assertEqual(response.status_code, 200)
	        self.assertEqual(response.templates[0].name, 'Empty POST Template')
	        self.assertTemplateNotUsed(response, 'Empty GET Template')
	        self.assertTemplateUsed(response, 'Empty POST Template')
	

	    def test_post(self):
	        "POST some data to a view"
	        post_data = {
	            'value': 37
	        }
	        response = self.client.post('/post_view/', post_data)
	

	        # Check some response details
	        self.assertEqual(response.status_code, 200)
	        self.assertEqual(response.context['data'], '37')
	        self.assertEqual(response.templates[0].name, 'POST Template')
	        self.assertContains(response, 'Data received')
	

	    def test_post_data_none(self):
	        msg = (
	            "Cannot encode None for key 'value' as POST data. Did you mean "
	            "to pass an empty string or omit the value?"
	        )
	        with self.assertRaisesMessage(TypeError, msg):
	            self.client.post('/post_view/', {'value': None})


def test_json_serialization(self):
	        """The test client serializes JSON data."""
	        methods = ('post', 'put', 'patch', 'delete')
	        tests = (
	            ({'value': 37}, {'value': 37}),
	            ([37, True], [37, True]),
	            ((37, False), [37, False]),
	        )
	        for method in methods:
	            with self.subTest(method=method):
	                for data, expected in tests:
	                    with self.subTest(data):
	                        client_method = getattr(self.client, method)
	                        method_name = method.upper()
	                        response = client_method('/json_view/', data, content_type='application/json')
	                        self.assertEqual(response.status_code, 200)
	                        self.assertEqual(response.context['data'], expected)
	                        self.assertContains(response, 'Viewing %s page.' % method_name)
	

	    def test_json_encoder_argument(self):
	        """The test Client accepts a json_encoder."""
	        mock_encoder = mock.MagicMock()
	        mock_encoding = mock.MagicMock()
	        mock_encoder.return_value = mock_encoding
	        mock_encoding.encode.return_value = '{"value": 37}'
	

	        client = self.client_class(json_encoder=mock_encoder)
	        # Vendored tree JSON content types are accepted.
	        client.post('/json_view/', {'value': 37}, content_type='application/vnd.api+json')
	        self.assertTrue(mock_encoder.called)
	        self.assertTrue(mock_encoding.encode.called)
	

	    def test_put(self):
	        response = self.client.put('/put_view/', {'foo': 'bar'})
	        self.assertEqual(response.status_code, 200)
	        self.assertEqual(response.templates[0].name, 'PUT Template')
	        self.assertEqual(response.context['data'], "{'foo': 'bar'}")
	        self.assertEqual(response.context['Content-Length'], '14')
	

	    def test_trace(self):
	        """TRACE a view"""
	        response = self.client.trace('/trace_view/')
	        self.assertEqual(response.status_code, 200)
	        self.assertEqual(response.context['method'], 'TRACE')
	        self.assertEqual(response.templates[0].name, 'TRACE Template')
	

	    def test_response_headers(self):
	        "Check the value of HTTP headers returned in a response"
	        response = self.client.get("/header_view/")
	

	        self.assertEqual(response['X-DJANGO-TEST'], 'Slartibartfast')
	

	    def test_response_attached_request(self):
	        """
	        The returned response has a ``request`` attribute with the originating
	        environ dict and a ``wsgi_request`` with the originating WSGIRequest.
	        """
	        response = self.client.get("/header_view/")
	

	        self.assertTrue(hasattr(response, 'request'))
	        self.assertTrue(hasattr(response, 'wsgi_request'))
	        for key, value in response.request.items():
	            self.assertIn(key, response.wsgi_request.environ)
	            self.assertEqual(response.wsgi_request.environ[key], value)
	

	    def test_response_resolver_match(self):
	        """
	        The response contains a ResolverMatch instance.
	        """
	        response = self.client.get('/header_view/')
	        self.assertTrue(hasattr(response, 'resolver_match'))
	

