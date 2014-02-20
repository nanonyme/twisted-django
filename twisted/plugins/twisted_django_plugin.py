from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor
from twisted.web.resource import Resource, getChildForRequest
from django.conf import settings
from urlparse import urlparse

class Options(usage.Options):
    optParameters = [["port", "p", 8000, "The port number to listen on."]]

class DjangoResource(Resource):
    def __init__(self, wsgi, static=None):
        Resource.__init__(self)
        self.wsgi = wsgi
        self.static = static

    def getChild(self, path, request):
        resource = getChildForRequest(self.static, request)
        if not hasattr(resource, "isdir") or resource.isdir() or not resource.exists():
            resource = self.wsgi
        return resource

class TwistedDjangoServiceMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = "twisted-django"
    description = "Starts Django WSGI in Twisted.web with static file handling"
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer.
        """
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        wsgi_resource = WSGIResource(reactor, reactor.getThreadPool(), application)

        static_url = getattr(settings, "STATIC_URL", "")
        if static_url and not urlparse(static_url).scheme:
            root = DjangoResource(wsgi_resource, File(settings.STATIC_ROOT))
        else:
            root = DjangoResource(wsgi_resource)
        site = Site(root)
        return internet.TCPServer(int(options["port"]), site)

serviceMaker = TwistedDjangoServiceMaker()
