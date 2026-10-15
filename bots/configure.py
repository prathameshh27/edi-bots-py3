"""
Bots configure lib
"""
import os
import sys

from . import botsinit, botsglobal, botslib


def bots_info(configdir=None, **kwargs):
    """
    Display Bots Environment informations.
    """
    kwargs.setdefault('interactive', True)
    configdir = botsinit.initbotsenv(**kwargs)
    if configdir:
        botsinit.generalinit(configdir)
        infos = f"{os.linesep}---------- [Bots Environment] ----------{os.linesep}"
        infos += os.linesep.join([f"    {key:22}: {value}" for key, value in botslib.botsinfo()])
        infos += os.linesep + "-" * 40
        return infos
    return f"Bots env not configured for config dir: {kwargs.get('configdir')}"


def start():
    """
    Configure bots environement and display config.
    """
    usage = """
This is "%(name)s" version %(version)s,

    Usage:
        %(name)s [botsenv-option]

        --help|-h|?|/?                          Display this help.

    botsenv-option:
        botsenv=<botsenv>                       Used alone to make botsenv_path = ~/.bots/env/<botsenv>/
        botsenv_path=<botsenv_path>             Bots env Root dir for (config/, botssys/, usersys/)
        -c<directory>|configdir=<directory>     Bots config directory of configuration files:
            (default: <botsenv_path>/config|~/.bots/env/<botsenv>|$USER|default/config)

        -y|--yes                                Skip interactive mode and keep going with positive reponse.
    """ % {
        'name': os.path.basename(sys.argv[0]),
        'version': botsglobal.version,
    }
    # (not in locals(): what is written there is lost in python >= 3.13)
    options = {'interactive': True}
    for arg in sys.argv[1:]:
        if arg.startswith('-c'):
            options['configdir'] = arg[2:]
        elif '=' in arg:
            arg, val = arg.split('=', 1)
            if arg not in ['configdir', 'botsenv', 'botsenv_path']:
                print(usage)
                return
            options[arg] = val
        elif arg in ['-y', '--yes']:
            options['interactive'] = False
        elif arg in ['?', '/?', '-h', '--help']:
            print(usage)
            return

    options['configdir'] = botsinit.initbotsenv(**options)
    if options['configdir']:
        print(bots_info(**options), file=sys.stderr)
