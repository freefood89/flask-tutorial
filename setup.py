from distutils.core import setup

setup(name='tutorial',
      version='1.0',
      description='A tutorial flask app',
      author='freefood89',
      packages=['tutorial'],
      install_requires=[
        "flask",
        "Flask-OAuthlib",
        "flask_sqlalchemy",
        "flask_migrate",
      ]
     )
