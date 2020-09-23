from flask import current_app, g, render_template

from .vendor.django_mail import get_connection
from .vendor.django_mail.message import EmailMultiAlternatives


def notify_newdle_participants(
    newdle, subject, text_template, html_template, get_context, attachments=None
):
    if not attachments:
        attachments = []
    participants = [p for p in newdle.participants if p.email]
    if not participants:
        return 0
    sender_name = newdle.creator_name
    reply_to = g.user['email']  # XXX this is kind of ugly
    emails = [
        create_email(
            sender_name,
            reply_to,
            participant.email,
            subject,
            text_template,
            html_template,
            get_context(participant),
            attachments,
        )
        for participant in participants
    ]
    return send_emails(emails)


def notify_newdle_creator(participant, subject, text_template, html_template, context, attachments=None):
    if not attachments:
        attachments = []
    creator_email = participant.newdle.creator_email
    sender_name = current_app.config['NOREPLY_ADDRESS']

    email = create_email(
        sender_name,
        participant.email,
        creator_email,
        subject,
        text_template,
        html_template,
        context,
        attachments,
    )

    return send_emails([email])


def send_emails(emails):
    with get_connection() as conn:
        return conn.send_messages(emails)


def create_email(
    sender_name,
    sender_email,
    recipient_email,
    subject,
    text_template,
    html_template,
    context,
    attachments,
):
    text_content = render_template(text_template, **context)
    html_content = render_template(html_template, **context)
    noreply_email = current_app.config['NOREPLY_ADDRESS']
    sender_name = sender_name.replace('"', '')
    from_email = f'"{sender_name} (via newdle)" <{noreply_email}>'
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email=from_email,
        to=[recipient_email],
        reply_to=[sender_email],
        attachments=attachments,
    )
    msg.attach_alternative(html_content, 'text/html')
    return msg
