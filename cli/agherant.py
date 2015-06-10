import click
import logging

from utils import config_utils
from utils.loggers import initLoggers
from webant.agherant_standalone import main
from custom_types import StringList


@click.command(help="launch agherant in standalone mode")
@click.version_option()
@click.option('-s', '--settings', type=click.Path(exists=True, readable=True), metavar="<path>", help='file from wich load settings')
@click.option('-d', '--debug', is_flag=True, help='operate in debug mode')
@click.option('-p', '--port', type=click.IntRange(min=1, max=65535), metavar="<port>", help='port on which daemon will listen')
@click.option('--address', type=click.STRING, metavar="<address>", help='address on which daemon will listen')
@click.option('--agherant-descriptions', type=StringList(), metavar="<url>..", help='list of description urls of nodes to aggregate')
def agherant(settings, debug, port, address, agherant_descriptions):
    initLoggers(logNames=['config_utils'])
    conf = config_utils.load_configs('WEBANT_', path=settings)
    cliConf = {}
    if debug:
        cliConf['DEBUG'] = True
    if port:
        cliConf['PORT'] = port
    if address:
        cliConf['ADDRESS'] = address
    if agherant_descriptions:
        cliConf['AGHERANT_DESCRIPTIONS'] = agherant_descriptions
    conf.update(cliConf)
    initLoggers(logging.DEBUG if conf.get('DEBUG', False) else logging.WARNING)
    try:
        main(conf)
    except Exception as e:
        if conf.get('DEBUG', False):
            raise
        else:
            click.secho(str(e), fg='yellow', err=True)

if __name__ == '__main__':
    agherant()
