"""Mail through the engine without a mail server: `mimefile` channels write and read complete emails as files.

Outgoing: file -> mimefile for each value of the channel field 'as body or as attachment'.
Incoming: emails with unusual headers -> mimefile -> file.
What is expected is what bots 3.2.0 did with the same channels and emails (measured in the migration audit).
"""
import email
import os

PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'\r\nUNZ+0+1'\r\n"


PARTNERS = [dict(idpartner='SENDER', active=True, name='sender', mail='sender@example.com'),
            dict(idpartner='RCVR', active=True, name='receiver', mail='rcvr@example.com')]


def test_outgoing_mail_body_or_attachment(botsrun):
    src = botsrun.path('src')
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    settings = {'blank': '', 'attachment': 'attachment', 'body': 'body', 'multipart': 'multipart',
                'multipart_attach': 'multipart_attach'}
    channels, routes = [], []
    for name, value in settings.items():
        channels += [
            dict(idchannel=name + '_in', inorout='in', type='file', path=src, filename='*.edi'),
            dict(idchannel=name + '_out', inorout='out', type='mimefile', path=botsrun.path('out', name),
                 filename='{infilename}', sendmdn=value),
        ]
        routes.append(dict(idroute=name, seq=1, active=True, fromchannel=name + '_in', tochannel=name + '_out',
                           translateind=2, frompartner='SENDER', topartner='RCVR'))
    botsrun.configure(partners=PARTNERS, channels=channels, routes=routes)
    assert botsrun.engine() == 0, botsrun.root

    found = {}
    for name in settings:
        files = os.listdir(botsrun.path('out', name))
        assert len(files) == 1, (name, files)
        with open(os.path.join(botsrun.path('out', name), files[0]), 'rb') as f:
            msg = email.message_from_binary_file(f)
        parts = [part for part in msg.walk() if not part.is_multipart()]
        assert len(parts) == 1 and parts[0].get_payload(decode=True) == PAYLOAD, name
        found[name] = (msg.get_content_type().startswith('multipart/'), parts[0].get_content_disposition(),
                       parts[0].get_filename())
    assert found == {
        'blank': (False, 'attachment', 'order.edi'),             # not set: attachment, as bots 3.x
        'attachment': (False, 'attachment', 'order.edi'),
        'body': (False, None, None),
        'multipart': (True, None, None),
        'multipart_attach': (True, 'attachment', 'order.edi'),
    }


def make_mail(subject=None, message_id='<1@example.com>', body=PAYLOAD):
    lines = [b'From: sender@example.com', b'To: rcvr@example.com', b'Date: Thu, 01 Jan 2026 12:00:00 +0000',
             b'MIME-Version: 1.0']
    if subject is not None:
        lines.append(b'Subject: ' + subject)
    if message_id is not None:
        lines.append(b'Message-ID: ' + message_id.encode('ascii'))
    lines += [b'Content-Type: application/edifact', b'Content-Disposition: attachment; filename="order.edi"',
              b'Content-Transfer-Encoding: 8bit', b'', body]
    return b'\r\n'.join(lines)


MAILS = {
    'plain': make_mail(b'order 1'),
    'encoded': make_mail(b'=?utf-8?q?caf=C3=A9?='),
    'mixed': make_mail(b'RE: =?utf-8?q?caf=C3=A9?= order'),          # plain text and an encoded word
    'nosubject': make_mail(None),
    'nomessageid': make_mail(b'order 2', message_id=None),
}


def test_incoming_mail_with_unusual_headers(botsrun):
    inbox = botsrun.path('inbox')
    for name, raw in MAILS.items():
        with open(os.path.join(inbox, name + '.eml'), 'wb') as f:
            f.write(raw)
    botsrun.configure(
        partners=PARTNERS,
        channels=[dict(idchannel='mail_in', inorout='in', type='mimefile', path=inbox, filename='*.eml'),
                  dict(idchannel='file_out', inorout='out', type='file', path=botsrun.path('out'), filename='*.edi')],
        chanpar=[dict(idpartner='SENDER', idchannel='mail_in', mail='sender@example.com'),
                 dict(idpartner='RCVR', idchannel='mail_in', mail='rcvr@example.com')],
        routes=[dict(idroute='mailin', seq=1, active=True, fromchannel='mail_in', tochannel='file_out', translateind=2)],
    )
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    delivered = os.listdir(botsrun.path('out'))
    assert len(delivered) == len(MAILS)
    for name in delivered:
        with open(os.path.join(botsrun.path('out'), name), 'rb') as f:
            assert f.read() == PAYLOAD, 'attachment is delivered unchanged, CRLF included'


def mails_in(directory):
    """the mails in directory, oldest first: [(content type, [(content type of part, payload of part)])]"""
    found = []
    for name in sorted(os.listdir(directory), key=lambda name: os.path.getmtime(os.path.join(directory, name))):
        with open(os.path.join(directory, name), 'rb') as f:
            msg = email.message_from_bytes(f.read())
        found.append((msg.get_content_type(), [(part.get_content_type(), part.get_payload(decode=True))
                                               for part in msg.walk() if not part.is_multipart()]))
    return found


def test_outgoing_mail_without_mime_encoding_keeps_the_content(botsrun):
    """mime encoding 'never': the bytes of the file are in the mail as they are"""
    src = botsrun.path('src')
    contents = {
        'lf.edi': b"UNB+UNOA:2+S+R+260101:1200+1'\nUNZ+0+1'\n",
        'cr.edi': b"UNB+UNOA:2+S+R+260101:1200+1'\rUNZ+0+1'\r",
        'crlf.edi': b"UNB+UNOA:2+S+R+260101:1200+1'\r\nUNZ+0+1'\r\n",
        'bytes.edi': bytes(range(1, 256)) + b'\n.\nFrom here\n',
    }
    for name, content in contents.items():
        with open(os.path.join(src, name), 'wb') as f:
            f.write(content)
    channels, routes = [dict(idchannel='f_in', inorout='in', type='file', path=src, filename='*.edi')], []
    for kind in ('attachment', 'multipart_attach'):
        channels.append(dict(idchannel='m_' + kind, inorout='out', type='mimefile', path=botsrun.path('out', kind),
                             filename='{infile}', sendmdn=kind, askmdn='never'))
        routes.append(dict(idroute=kind, seq=1, active=True, fromchannel='f_in', tochannel='m_' + kind,
                           translateind=2, frompartner='SENDER', topartner='RCVR'))
    botsrun.configure(partners=PARTNERS, channels=channels, routes=routes)
    assert botsrun.engine() == 0, botsrun.root
    for kind in ('attachment', 'multipart_attach'):
        directory = botsrun.path('out', kind)
        assert sorted(os.listdir(directory)) == sorted(contents)
        for name, content in contents.items():
            with open(os.path.join(directory, name), 'rb') as f:
                mail = f.read()
            assert mail.count(content) == 1, (kind, name)
            if kind == 'attachment':
                assert mail.endswith(b'\r\n\r\n' + content), name


def test_resend_of_a_mail_is_the_same_mail(botsrun):
    """resend: the document is send in a mail again; not: the old mail as attachment in a new mail.
    Also for a mail made by bots 3 (it has no mark that it is an assembled mail)."""
    src, out = botsrun.path('src'), botsrun.path('out')
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    botsrun.configure(
        partners=PARTNERS,
        channels=[dict(idchannel='f_in', inorout='in', type='file', path=src, filename='*.edi', remove=True),
                  dict(idchannel='m_out', inorout='out', type='mimefile', path=out, filename='mail_{idta}.eml')],
        routes=[dict(idroute='mailout', seq=1, active=True, fromchannel='f_in', tochannel='m_out', translateind=2,
                     frompartner='SENDER', topartner='RCVR')])
    assert botsrun.engine() == 0, botsrun.root
    first = mails_in(out)
    assert len(first) == 1 and first[0][1][0][1] == PAYLOAD
    expected = first[0]

    # the user asks for a resend in the web interface
    externout = 520          # botsconfig.EXTERNOUT
    botsrun.side('sql', 'UPDATE ta SET retransmit=1 WHERE status=%s' % externout)
    assert botsrun.engine('--resend') == 0, botsrun.root
    assert mails_in(out) == [expected, expected]

    # the same for the mail as bots 3 stored it: without the mark (rsrv2) and with the content type of the document
    botsrun.side('sql', "UPDATE ta SET rsrv2=0, contenttype='application/edifact' WHERE rsrv2=1",
                 'UPDATE ta SET retransmit=1 WHERE status=%s AND statust=3 AND idta=(SELECT MAX(idta) FROM ta WHERE '
                 'status=%s)' % (externout, externout))
    assert botsrun.engine('--resend') == 0, botsrun.root
    assert mails_in(out) == [expected, expected, expected]
