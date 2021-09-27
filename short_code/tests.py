import json

from django.test import TestCase, override_settings
from short_code.models import ShortCode, DynamicConfig, InitialParametersState


@override_settings(ALPHABET='ABCDEF0123456789')
@override_settings(SORTED_ALPHABET='0123456789ABCDEF')
@override_settings(REQUESTED_SHORT_CODE_LENGTH=3)
@override_settings(CHECK_SHORT_CODE_LENGTH_PROVIDED_BY_USER=True)
class TestShortCode(TestCase):

    def test_custom_validators(self):
        # Url not present
        response = self.client.post(
            '/api/short_code/shorten/', data={}
        )
        expected = '{"detail":"Url not present"}'
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf8'), expected)

        # Invalid url
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http//google.com'}
        )
        expected = '{"detail":"The provided url is invalid"}'
        self.assertEqual(response.status_code, 412)
        self.assertEqual(response.content.decode('utf8'), expected)

        # Short code unexpected symbol
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://google.com', 'shortcode': '12K'}
        )
        expected = '{"detail":"The provided short code is invalid. Unexpected symbol \'K\'"}'
        self.assertEqual(response.status_code, 412)
        self.assertEqual(response.content.decode('utf8'), expected)

        # Short code unexpected length
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://google.com', 'shortcode': '12AB'}
        )
        expected = '{"detail":"The provided short code is invalid. Unexpected length 4"}'
        self.assertEqual(response.status_code, 412)
        self.assertEqual(response.content.decode('utf8'), expected)

    def test_short_code_creation(self):
        # 000
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://link-0.com'}
        )
        expected = '{"shortcode":"000"}'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content.decode('utf8'), expected)

        short_code = ShortCode.objects.get(short_code='000')
        self.assertEqual(short_code.full_url, 'http://link-0.com')
        self.assertEqual(short_code.redirect_count, 0)
        self.assertEqual(ShortCode.objects.all().count(), 1)

        # 001
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://link-1.com'}
        )
        expected = '{"shortcode":"001"}'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content.decode('utf8'), expected)

        short_code = ShortCode.objects.get(short_code='001')
        self.assertEqual(short_code.full_url, 'http://link-1.com')
        self.assertEqual(short_code.redirect_count, 0)
        self.assertEqual(ShortCode.objects.all().count(), 2)

        # 002
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://link-2.com', 'shortcode': '002'}
        )
        expected = '{"shortcode":"002"}'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content.decode('utf8'), expected)

        short_code = ShortCode.objects.get(short_code='002')
        self.assertEqual(short_code.full_url, 'http://link-2.com')
        self.assertEqual(short_code.redirect_count, 0)
        self.assertEqual(ShortCode.objects.all().count(), 3)

        # 003
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://link-3.com', 'shortcode': '003'}
        )
        expected = '{"shortcode":"003"}'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content.decode('utf8'), expected)

        short_code = ShortCode.objects.get(short_code='003')
        self.assertEqual(short_code.full_url, 'http://link-3.com')
        self.assertEqual(short_code.redirect_count, 0)
        self.assertEqual(ShortCode.objects.all().count(), 4)

        # 004
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://link-4.com'}
        )
        expected = '{"shortcode":"004"}'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content.decode('utf8'), expected)

        short_code = ShortCode.objects.get(short_code='004')
        self.assertEqual(short_code.full_url, 'http://link-4.com')
        self.assertEqual(short_code.redirect_count, 0)
        self.assertEqual(ShortCode.objects.all().count(), 5)

        initial_parameter_id = DynamicConfig.objects.get(name=DynamicConfig.CURRENT_INITIAL_PARAMETERS_ID).value
        initial_parameters_state = InitialParametersState.objects.get(id=initial_parameter_id)
        self.assertEqual(InitialParametersState.objects.all().count(), 1)

        self.assertEqual(initial_parameters_state.alphabet_sorted, '0123456789ABCDEF')
        self.assertEqual(initial_parameters_state.requested_short_code_length, 3)
        self.assertEqual(initial_parameters_state.min_number_from_range, 0)
        self.assertEqual(initial_parameters_state.max_number_from_range, 4095)
        self.assertEqual(initial_parameters_state.last_number_converted_to_short_code, 4)

        # Bad Request
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://link-new.com', 'shortcode': '004'}
        )
        expected = '{"detail":"Short code already in use"}'
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content.decode('utf8'), expected)

        # Far number don't have impact on 'last_number_converted_to_short_code
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': 'http://link-new.com', 'shortcode': 'A4E'}
        )
        expected = '{"shortcode":"A4E"}'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content.decode('utf8'), expected)

        initial_parameters_state = InitialParametersState.objects.get(id=initial_parameter_id)
        self.assertEqual(InitialParametersState.objects.all().count(), 1)
        self.assertEqual(initial_parameters_state.last_number_converted_to_short_code, 4)

    def test_redirect_and_stats(self):
        short_code = 'BF5'
        full_url = 'http://link-test.com'

        # Create Short Code
        response = self.client.post(
            '/api/short_code/shorten/',
            data={'url': full_url, 'shortcode': short_code}
        )
        expected = '{"shortcode":"%s"}' % short_code
        self.assertEqual(response.content.decode('utf8'), expected)
        self.assertEqual(response.status_code, 201)

        # Get Stats 1
        response = self.client.get(
            '/api/short_code/%s/stats' % short_code
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_body['redirectCount'], 0)
        created_string_first_call = response_body['created']
        self.assertIsNone(response_body['lastRedirect'])

        # Get Redirect 1
        response = self.client.get(
            '/api/short_code/%s' % short_code
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, full_url)

        # Get Redirect 2
        response = self.client.get(
            '/api/short_code/%s' % short_code
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, full_url)

        # Get Redirect 3
        self.client.get(
            '/api/short_code/%s' % short_code
        )

        # Get Stats
        response = self.client.get(
            '/api/short_code/%s/stats' % short_code
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_body['redirectCount'], 3)
        created_string_second_call = response_body['created']
        self.assertIsNotNone(response_body['lastRedirect'])

        self.assertEqual(created_string_first_call, created_string_second_call)
        self.assertIsInstance(created_string_first_call, str)
