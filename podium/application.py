import logging

from errors import UnsupportedWebAppError

logger = logging.getLogger(__name__)


class ApplicationAdapter(object):
    def __init__(self, web_app=None):
        self.web_app = web_app

    def run_web(self, host='127.0.0.1', port=8000, reload=True, reload_interval=1, debug=True, **kwargs):
        raise NotImplementedError("This app does not support web")

    def run_wsgi(self):
        raise NotImplementedError("This app does not support web")

    def run_cli(self, argv=None):
        pass


class CLIApplication(ApplicationAdapter):
    pass


class BottleApplication(ApplicationAdapter):
    def run_web(self, host='127.0.0.1', port=8000, reloader=True, reload_interval=1, debug=True, **kwargs):
        self.web_app.run(host=host, port=port, interval=reload_interval, reloader=reloader, debug=debug, **kwargs)

    def run_wsgi(self):
        return self.web_app


class Application(object):
    def __init__(self, web_app=None):
        if web_app:
            if web_app.__class__.__name__ == 'Bottle':
                self.app = BottleApplication(web_app)
            else:
                raise UnsupportedWebAppError(web_app)
        else:
            self.app = CLIApplication()

    def __getattr__(self, key):
        return getattr(self.app, key)

    def __setattr__(self, key, value):
        return setattr(self.app, key, value)
