class PodiumError(Exception):
    pass


class MissingModuleError(PodiumError):
    def __init__(self, in_module, missing_module):
        super(MissingModuleError, self).__init__("The module '%s' required '%s' to function and it cannot be imported.  Many required modules are not requirements of podium itself but must be independently required or installed." % (in_module, missing_module))


class UnrecognizedPluginError(PodiumError):
    def __init__(self, plugin):
        super(UnsupportedWebAppError, self).__init__("Unrecognized plugin: '%s'" % (plugin,))
