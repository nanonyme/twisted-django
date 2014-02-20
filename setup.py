from setuptools import setup

setup(name='twisted-django',
      version='0.1',
      description='Django Twisted integration layer',
      author='Seppo Yli-Olli',
      author_email='seppo.yli-olli@iki.fi',
      url='http://github.com/nanonyme/twisted-django',
      packages=['twisted.plugins'],
      install_requires=["Twisted", "Django"],
     )

try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))
