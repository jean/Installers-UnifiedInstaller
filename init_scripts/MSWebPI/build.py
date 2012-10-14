import sys
import os
import subprocess
import shutil
import logging

logger = logging.getLogger('Plone.UnifiedInstaller')


def main():
    CWD = os.getcwd()
    UIDIR = os.path.dirname(os.path.dirname(os.path.abspath(CWD)))
    PLONE_HOME = os.path.join(CWD, 'Plone.msdeploy', 'PloneApp')
    INSTANCE_HOME = os.path.join(PLONE_HOME, 'zinstance')
    CLIENT_USER = os.environ['USERNAME']
    ZEO_USER = ROOT_INSTALL = OFFLINE = CLIENTS = "0"
    RUN_BUILDOUT = "0"
    INSTALL_LXML = "no"
    ITYPE = "standalone"
    LOG_FILE = os.path.join(PLONE_HOME, 'install.log')
    BUILDOUT_DIST = os.path.join(
        PLONE_HOME, 'buildout-cache', 'downloads', 'dist')

    PASSWORD = subprocess.check_output([
        sys.executable,
        os.path.join(UIDIR, 'helper_scripts', 'generateRandomPassword.py')])

    if os.path.exists(INSTANCE_HOME):
        shutil.rmtree(INSTANCE_HOME)
    subprocess.check_call([
        sys.executable,
        os.path.join(UIDIR, 'helper_scripts', 'create_instance.py'),
        UIDIR, PLONE_HOME, INSTANCE_HOME, CLIENT_USER, ZEO_USER,
        PASSWORD, ROOT_INSTALL, RUN_BUILDOUT, INSTALL_LXML, OFFLINE,
        ITYPE, LOG_FILE, CLIENTS])

    if not os.path.exists(BUILDOUT_DIST):
        os.makedirs(BUILDOUT_DIST)

    logger.info('Delegating to Web Deploy Package script: {0}'.format(
        os.path.join(PLONE_HOME, 'iis_deploy.py')))
    try:
        os.chdir(PLONE_HOME)
        subprocess.check_call([sys.executable, 'iis_deploy.py'])
    finally:
        os.chdir(CWD)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
