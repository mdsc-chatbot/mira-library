from django.core import mail
from django.test import TestCase


class EmailTest(TestCase):
    """
    Checks for Email Operations
    """

    def test_send_email(self):
        """
        This method tests for email sending fields
        :return: None
        """

        # Creating a test container for email information
        email = mail.EmailMessage(
            subject='Send Email Testing',
            body='This is a test message.',
            # from_email='from@test.ca',
            to=['to@test.ca'],
        )

        # Email was sent successfully
        self.assertTrue(email.send())

        # Checking if the outbox has an email stored
        self.assertEqual(len(mail.outbox), 1)
        # Checking the outbox mail information with the original email information
        self.assertEqual(mail.outbox[0].subject, email.subject)
        self.assertEqual(mail.outbox[0].body, email.body)
        self.assertEqual(mail.outbox[0].from_email, email.from_email)
        self.assertListEqual(mail.outbox[0].to, email.to)
