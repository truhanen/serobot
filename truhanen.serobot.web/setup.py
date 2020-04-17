
from setuptools import setup, find_namespace_packages, Command
from setuptools.command.install import install
from setuptools.command.develop import develop
import subprocess
from pathlib import Path


frontend_dpath = Path(__file__).parent / 'truhanen' / 'serobot' / 'web' / 'frontend'
frontend_dist_dpath = frontend_dpath / 'dist'


def build_frontend():
    """Run the npm build command. Raise an error if the npm build fails,
    e.g. if npm is not available.
    """
    # Check that npm is installed.
    npm_version_process = subprocess.run(
        'npm --version', shell=True, capture_output=True)
    if npm_version_process.returncode != 0:
        raise RuntimeError('Couldn\'t find an npm installation on this system. '
                           'You either need the frontend to be built somewhere '
                           'else, or a functional npm installation to build '
                           'the frontend here. Check README.md for more '
                           'information.')
    # Run the npm build command.
    npm_build_command = f'npm run build --prefix {frontend_dpath}'
    print(f'Building the frontend with "{npm_build_command}"')
    npm_build_process = subprocess.run(
        npm_build_command, shell=True, capture_output=False)
    if npm_build_process.returncode != 0:
        raise RuntimeError(
            f'Building the frontend with "{npm_build_command}" '
            f'failed with exit code {npm_build_process.returncode}. '
            f'Stderr:\n{npm_build_process.stderr}')


def check_and_build_frontend():
    """Check that the frontend build directory exists. If it doesn't, try
    to build it.
    """
    if not frontend_dist_dpath.exists():
        build_frontend()


# Customized install command to ensure the frontend is built
class InstallCommand(install):
    def run(self):
        if not self.skip_build:
            check_and_build_frontend()
        super().run()


# Customized develop command to ensure the frontend is built
class DevelopCommand(develop):
    def run(self):
        if not self.uninstall:
            check_and_build_frontend()
        super().run()


class BuildFrontendCommand(Command):
    description = 'build only the frontend using npm'
    user_options = []
    def run(self):
        build_frontend()
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    subcommands = []


setup(
    name='truhanen.serobot.web',
    version='0.1.0',
    author='Tuukka Ruhanen',
    author_email='tuukka.t.ruhanen@gmail.com',
    description='Web server & UI for controlling a Raspberry Pi robot.',
    install_requires=[
        # Serobot API
        'truhanen.serobot.api',
        # Web server
        'aiohttp',
        'aiohttp_security',
        'aiohttp_session',
        'cryptography',
    ],
    packages=find_namespace_packages(),
    package_data={
        'truhanen.serobot.web': [
            'frontend/dist/*',
            'frontend/dist/*/*',
        ]},
    scripts=[
        str(Path(__file__).parent / 'scripts' / 'start_serobot_server'),
    ],
    cmdclass={
        'install': InstallCommand,
        'build_frontend': BuildFrontendCommand,
        'develop': DevelopCommand,
    },
    zip_safe=False,
)
