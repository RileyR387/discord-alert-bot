
import os
import sys
import yaml
import re

##
def LoadConfig(confFile: str) -> dict:
    """
    Load some YAML, or return None
    """
    if isinstance( confFile, list):
        return SearchConfigs( confFile )

    try:
        with open( confFile, 'r') as stream:
            return yaml.load(stream, Loader=yaml.SafeLoader);
    except OSError as e:
        # TODO: Log location with trace or debug level?
        return None
    except Exception as e:
        print( "Failed to load config with error: {}".format(e))
        return None

def SearchConfigs(searchPaths: list) -> dict:
    """
    Given an array of search locations, try to load files, first file to load is returned.
    """
    config = None;

    if isinstance(searchPaths, list):

        for path in searchPaths:
            if config is None:
                config = LoadConfig( path )
                if config is not None:
                    return config;

        if config is None:
            print( "Failed to load config, searched: ['%s']" % "', '".join(searchPaths), file=sys.stderr)

    else:
        return LoadConfig(searchPaths)

def MergeConfigs(searchPaths: list) -> dict:
    """
    Given an array of search locations, files are "merged" first to last, if they exists.
    Any keys defined in last config will overwrite values
    in the first config, including blank and False values.
    If a key exists in the first config that isn't overwritten by a later config, it will be included in final configuration.

    - Usefor for ['default.yaml','app.PROD.yaml'] ect
    """
    config = None;

    if isinstance( searchPaths, list):
        for path in searchPaths:
            if config is None:
                config = LoadConfig( path )
            else:
                overlayConf = LoadConfig( path )
                if overlayConf is not None:
                    config.update( overlayConf )

        if config is None:
            print( "Failed to merge any config, : ['%s']" % "', '".join(searchPaths), file=sys.stderr)

    else:
        return LoadConfig(searchPaths)

    return config

def AutoLoad(scriptName: str) -> dict:
    """
    Attempt to autoload yaml config based on typical search paths/conventions
    """
    scriptName = os.path.basename(scriptName)
    scriptName = re.sub(r"\.py$","", scriptName)

    defaultPaths = [
        './default.yaml',
        './etc/' + scriptName + '.yaml',
        os.path.expanduser('~/etc/' + scriptName + '.yaml'),
        os.path.expanduser('~/.' + scriptName + '.yaml'),
        '/etc/' + scriptName + '.yaml'
    ]
    return MergeConfigs(defaultPaths)

