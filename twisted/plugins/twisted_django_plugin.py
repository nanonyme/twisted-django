from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor
from twisted.web.tap import makePersonalServerFactory
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from urlparse import urlparse

class Options(usage.Options):
    optParameters = [["port", "p", 8080, "The port number to listen on."]]

class TwistedDjangoServiceMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = "twisted-django"
    description = "Starts Django WSGI in Twisted.web with static file handling"
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer.
        """
        application = get_wsgi_application()
        wsgi_resource = WSGIResource(reactor, reactor.getThreadPool(), application)
        site = Site(wsgi_resource)
        static_url = getattr(settings, "STATIC_URL", "")
        if static_url and not urlparse(static_url).scheme:
            site.putChild(static_url, File(settings.STATIC_ROOT))
        return internet.TCPServer(int(options["port"]), makePersonalServerFactory(site))

serviceMaker = TwistedDjangoServiceMaker()
