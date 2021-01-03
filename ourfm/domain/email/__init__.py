import requests

from flask import current_app as app

logger = app.logger


def send(*, subject,
         from_, to=None, cc=None, bcc=None,
         text_content=None, html_content=None,
         inline=None, attachments=None,
         tags=None):
    """Sends an email message using the Mailgun API.

    Args:
        subject(str): subject line
        from_(str): email address of the sender
        to_(str): email address of the recipient
        cc(str): email address to receive a copy
        bcc(str): email address to receive a blind copy
        text_content(str): text version of the message
        html_content(str): html version of the message
        inline(list of tuple): assets referenced in the html message, see below
        attachments(list of tuple): files to attach to the email, see below
        tags(list of tuple): tags to apply to the email, for analytics

    Returns:
        (requests.models.response): response from the request

    The tuple for inline and attachments should be in the form:
        ('file.name'(str), file_content(bytes), 'MIME type'(str))
    eg:
        files = ('my.pdf', open('my.pdf', 'rb'), 'application/pdf')
    """
    if all((to is None, cc is None, bcc is None)):
        raise ValueError("At least one of `to`, `cc` or `bcc` must be supplied")

    if all((html_content is None, text_content is None)):
        raise ValueError("`html_content` or `text_content` or both must be supplied")

    endpoint = f"https://api.eu.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages"
    auth = ('api', app.config['MAILGUN_API_KEY'])

    if isinstance(tags, str):
        # tags need to be sent as a list
        tags = [tags]

    data = {'subject': subject,
            'from': from_,
            'to': to,
            'cc': cc,
            'bcc': bcc,
            'text': text_content,
            'html': html_content,
            'o:tag': tags}

    inline_files = label_email_files('inline', inline)
    attachment_files = label_email_files('attachment', attachments)
    files = inline_files + attachment_files

    resp = requests.post(endpoint, auth=auth, data=data, files=files)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        logger.error(e)

    return resp


def label_email_files(label, files):
    """Formats files into the format required by the Mailgun API.

    Args:
        label(str): label to use
        files(tuple or list of tuples): files to label

    Returns:
        (list of tuples): formatted file tuples
    """
    if files is None:
        return []

    if not isinstance(files, list):
        files = [files]

    return [(label, a) for a in files]
