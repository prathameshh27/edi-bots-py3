"""User scripts written for bots 3 (ported to python 3 syntax, nothing else) run in the engine."""
import os
import textwrap

PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"
MAIL = b'\r\n'.join([
    b'From: sender@example.com', b'To: rcvr@example.com', b'Date: Thu, 01 Jan 2026 12:00:00 +0000',
    b'Subject: order', b'Message-ID: <1@example.com>', b'MIME-Version: 1.0', b'Content-Type: application/edifact',
    b'Content-Disposition: attachment; filename="order.edi"', b'Content-Transfer-Encoding: 8bit', b'', PAYLOAD])


def userscript(botsrun, kind, name, text):
    directory = os.path.join(botsrun.envdir, 'usersys', kind)
    os.makedirs(directory, exist_ok=True)
    init = os.path.join(directory, '__init__.py')
    if not os.path.exists(init):
        open(init, 'w', encoding='utf8').close()
    with open(os.path.join(directory, name + '.py'), 'w', encoding='utf8') as f:
        f.write(textwrap.dedent(text))


def test_route_script_uses_start_of_route_and_routepart(botsrun):
    """botsglobal.currentrun.get_minta4query_route() / _routepart(), eg as rootidta in a route script"""
    src, out, note = botsrun.path('src'), botsrun.path('out'), os.path.join(botsrun.root, 'note.txt')
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    userscript(botsrun, 'routescripts', 'utroute', '''
        from bots import botsglobal, botslib
        import bots.usersys.routescripts as viaoldname

        def postincommunication(routedict):
            run = botsglobal.currentrun
            received = len(list(botslib.query(
                'SELECT idta FROM ta WHERE idta>%%(rootidta)s AND status=%%(status)s AND idroute=%%(idroute)s',
                {'rootidta': run.get_minta4query_routepart(), 'status': botslib.FILEIN, 'idroute': routedict['idroute']})))
            with open(r'%s', 'w') as f:
                f.write('%%s|%%s|%%s|%%s|%%s' %% (run.get_minta4query(), run.get_minta4query_route(),
                                              run.get_minta4query_routepart(), received, viaoldname.__file__))
        ''' % note)
    botsrun.configure(
        channels=[dict(idchannel='ut_in', inorout='in', type='file', path=src, filename='*.edi'),
                  dict(idchannel='ut_out', inorout='out', type='file', path=out, filename='*.edi')],
        routes=[dict(idroute='utroute', seq=1, active=True, fromchannel='ut_in', tochannel='ut_out', translateind=2)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    with open(note, encoding='utf8') as f:
        run, route, routepart, received, usersysfile = f.read().split('|')
    assert int(run) < int(route) < int(routepart)
    assert received == '1'
    # 'bots.usersys' is the usersys of the environment
    assert os.path.dirname(usersysfile) == os.path.join(botsrun.envdir, 'usersys', 'routescripts')
    assert os.listdir(out) == ['1.edi']


def test_accept_incoming_attachment_with_bots3_signature(botsrun):
    inbox, out = botsrun.path('inbox'), botsrun.path('out')
    with open(os.path.join(inbox, 'mail.eml'), 'wb') as f:
        f.write(MAIL)
    userscript(botsrun, 'communicationscripts', 'ut_mail_in', '''
        def accept_incoming_attachment(channeldict, ta, charset, content, contenttype):
            return contenttype == 'application/edifact'
        ''')
    botsrun.configure(
        partners=[dict(idpartner='SENDER', active=True, name='sender', mail='sender@example.com'),
                  dict(idpartner='RCVR', active=True, name='receiver', mail='rcvr@example.com')],
        channels=[dict(idchannel='ut_mail_in', inorout='in', type='mimefile', path=inbox, filename='*.eml'),
                  dict(idchannel='ut_file_out', inorout='out', type='file', path=out, filename='*.edi')],
        routes=[dict(idroute='utmail', seq=1, active=True, fromchannel='ut_mail_in', tochannel='ut_file_out',
                     translateind=2)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    assert len(os.listdir(out)) == 1


def test_subject_script_with_bots3_signatures(botsrun):
    """communication script 'subject' as installations of bots 3 have it: with and without *args/**kwargs,
    using ta.synall() and ta.botskey"""
    import email
    src = botsrun.path('src')
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    scripts = {
        'm_plain': '''
            import bots.botslib as botslib
            def subject(channeldict,ta,subjectstring,content):
                return 'shipment ' + str(ta.botskey)
            ''',
        'm_args': '''
            def subject(channeldict,ta,subjectstring,content,*args,**kwargs):
                ta.synall()        #needed to get access to attributes of object ta (eg ta.frompartner)
                return 'PREFIX' + '_' + subjectstring + '_' + ta.frompartner + '_' + channeldict['idchannel']
            ''',
        'm_or': '''
            def subject(channeldict,ta,subjectstring,content):
                return 'Order ' + (ta.botskey or subjectstring)
            ''',
    }
    channels = [dict(idchannel='f_in', inorout='in', type='file', path=src, filename='*.edi')]
    routes = []
    for name, text in scripts.items():
        userscript(botsrun, 'communicationscripts', name, text)
        channels.append(dict(idchannel=name, inorout='out', type='mimefile', path=botsrun.path('out', name),
                             filename='mail.eml'))
        routes.append(dict(idroute=name, seq=1, active=True, fromchannel='f_in', tochannel=name, translateind=2,
                           frompartner='SENDER', topartner='RCVR'))
    botsrun.configure(
        partners=[dict(idpartner='SENDER', active=True, name='sender', mail='sender@example.com'),
                  dict(idpartner='RCVR', active=True, name='receiver', mail='rcvr@example.com')],
        channels=channels, routes=routes)
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    subjects = {}
    for name in scripts:
        with open(os.path.join(botsrun.path('out', name), 'mail.eml'), 'rb') as f:
            subjects[name] = email.message_from_bytes(f.read())['subject']
    assert subjects['m_plain'] == 'shipment None' or subjects['m_plain'].startswith('shipment '), subjects
    assert subjects['m_args'].startswith('PREFIX_') and subjects['m_args'].endswith('_SENDER_m_args'), subjects
    assert subjects['m_or'].startswith('Order ') and len(subjects['m_or']) > len('Order '), subjects


def test_channel_class_overridden_in_a_communication_script(botsrun):
    """A communication script of bots 3 that replaces 'outcommunicate' of a channel type by its own (here for
    type file; an installation does it for sftp), written with the functions of bots 3."""
    src, out = botsrun.path('src'), botsrun.path('out')
    for name in ('a.edi', 'b.edi'):
        with open(os.path.join(src, name), 'wb') as f:
            f.write(PAYLOAD + name.encode())
    userscript(botsrun, 'communicationscripts', 'own_out', '''
        import posixpath
        import shutil
        from bots.botsconfig import *
        import bots.botslib as botslib
        import bots.communication as communication

        class file(communication.file):
            @botslib.log_session
            def outcommunicate(self):
                filename_mask = self.channeldict['filename'] if self.channeldict['filename'] else '*'
                if '{overwrite}' in filename_mask:
                    filename_mask = filename_mask.replace('{overwrite}','')
                for row in botslib.query(\'\'\'SELECT idta,filename,numberofresends
                                            FROM ta
                                            WHERE idta>%(rootidta)s
                                            AND status=%(status)s
                                            AND statust=%(statust)s
                                            AND tochannel=%(tochannel)s
                                            \'\'\',
                                            {'tochannel':self.channeldict['idchannel'],'rootidta':self.rootidta,
                                            'status':FILEOUT,'statust':OK}):
                    try:
                        ta_from = botslib.OldTransaction(row['idta'])
                        ta_to = ta_from.copyta(status=EXTERNOUT)
                        tofilename = 'own_' + self.filename_formatter(filename_mask,ta_from)
                        fromfilename = botslib.abspathdata(row['filename'])
                        shutil.copyfile(fromfilename, posixpath.join(self.channeldict['path'], tofilename))
                    except:
                        txt = botslib.txtexc()
                        ta_to.update(statust=ERROR,errortext=txt,numberofresends=row['numberofresends'] + 1)
                    else:
                        ta_to.update(statust=DONE,filename='file:/' + tofilename,numberofresends=row['numberofresends'] + 1)
                    finally:
                        ta_from.update(statust=DONE)
        ''')
    botsrun.configure(
        channels=[dict(idchannel='f_in', inorout='in', type='file', path=src, filename='*.edi'),
                  dict(idchannel='own_out', inorout='out', type='file', path=out, filename='{infile}')],
        routes=[dict(idroute='own', seq=1, active=True, fromchannel='f_in', tochannel='own_out', translateind=2)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    assert sorted(os.listdir(out)) == ['own_a.edi', 'own_b.edi']
    assert result['report']['send'] == 2


def test_channels_use_testpath_keeps_everything_on_this_machine(botsrun):
    """bots.ini [settings] channels_use_testpath: a channel uses its testpath; one without testpath is not run"""
    import re
    src, out, test_out = botsrun.path('src'), botsrun.path('out'), botsrun.path('test_out')
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    ini = os.path.join(botsrun.envdir, 'config', 'bots.ini')
    with open(ini, encoding='utf8') as f:
        text = f.read()
    text = re.sub(r'(?m)^runacceptancetest\s*=.*$', 'runacceptancetest = False', text)
    text = re.sub(r'(?m)^\[settings\]\s*$', '[settings]\nchannels_use_testpath = True', text, count=1)
    with open(ini, 'w', encoding='utf8') as f:
        f.write(text)
    botsrun.configure(
        channels=[dict(idchannel='f_in', inorout='in', type='file', path=src, filename='*.edi'),
                  # would connect to a server: with a testpath, writes to that folder
                  dict(idchannel='to_partner', inorout='out', type='sftp', host='partner.invalid', port=22,
                       username='u', secret='p', path='upload', filename='{infile}', testpath=test_out),
                  # without testpath: not run
                  dict(idchannel='no_testpath', inorout='out', type='ftp', host='partner.invalid', port=21,
                       username='u', secret='p', path='upload', filename='{infile}')],
        routes=[dict(idroute='safe', seq=1, active=True, fromchannel='f_in', tochannel='to_partner', translateind=2),
                dict(idroute='refused', seq=1, active=True, fromchannel='f_in', tochannel='no_testpath', translateind=2)])
    botsrun.engine()
    result = botsrun.result()
    assert os.listdir(test_out) == ['order.edi']
    assert any('channels_use_testpath' in text and 'no_testpath' in text for text in result['errors']), result['errors']
    assert not os.listdir(out)
