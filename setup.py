from setuptools import setup, Command

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import subprocess
        errno = subprocess.call(['py.test',  'testing'])
        raise SystemExit(errno)

setup(name='mock_fedorainfra',
      version='0.1.3',
      description='Mock Fedora infrastructure designed to test AutoQA',
      author='Tim Flink',
      author_email='tflink@fedoraproject.org',
      url='http://localhost/something',
      packages=['mock_fedorainfra', 'mock_fedorainfra.koji', 'mock_fedorainfra.bodhi'],
      package_dir={'mock_fedorainfra':'mock_fedorainfra'},
      include_package_data=True,
      cmdclass = {'test' : PyTest},
      install_requires = [
        'pytest>=2.0.3',
        'Flask>=0.8',
        'Flask-XML-RPC>=0.1.2',
        'SQLAlchemy >= 0.7'
     ]
     )
