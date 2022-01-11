import base64
from email.mime.text import MIMEText
import constants


def create_message(sender: str, to: str, subject: str, message_text: str):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def send_message(service: object, user_id: str, msg: dict):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg: Message to be sent.

    Returns:
        Sent Message.
    """

    message = (service.users().messages().send(userId=user_id, body=msg)
               .execute())
    return message


def send_mail(list_of_candidates: list, email_body: str, gmail_service: object):
    """Send an email message to multiple users

    Args:
        list_of_candidates: List of rows from Google Sheets file
        email_body: Body of the email
        gmail_service: Gmail service object
    """

    for candidate_info in list_of_candidates:
        body = email_body.replace('[NAME]', candidate_info[0].split(' ')[0])
        to_email = candidate_info[1]
        message = create_message('Writer Shark Outreach <outreach@writershark.com>', to_email,
                                 constants.EMAIL_SUBJECT, body)

        send_message(gmail_service, 'me', message)
