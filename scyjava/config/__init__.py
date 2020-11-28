__all__ = (
    'maven_scijava_repository',
    'add_endpoints',
    'get_endpoints',
    'add_repositories',
    'get_repositories',
    'set_verbose',
    'get_verbose',
    'set_manage_deps',
    'get_manage_deps',
    'set_cache_dir',
    'get_cache_dir',
    'set_m2_repo',
    'get_m2_repo',
    'set_options',
    'add_options',
    'get_options',
    'set_classpath',
    'add_classpath',
    'get_classpath')

import logging
import os
import platform
import pathlib
import jgo
import jpype
import jpype.imports
import subprocess

_logger = logging.getLogger(__name__)

_endpoints = []
_repositories = {1: 'https://maven.scijava.org/content/repositories/releases'}
_verbose = 0
_manage_deps = True
_cache_dir = pathlib.Path.home() / '.jgo'
_m2_repo = pathlib.Path.home() / '.m2' / 'repository'
_options = ''
_add_options = ''


def start_JVM(options=''):
    global _options
    _options = options

    # if JVM is already running -- break
    if JVM_status() == True:
        _logger.debug('The JVM is already running.')
        return

    # retrieve endpoint and repositories from scyjava config
    endpoints = get_endpoints()
    repositories = get_repositories()

    # use the logger to notify user that endpoints are being added
    _logger.debug('Adding jars from endpoints {0}'.format(endpoints))

    # get endpoints and add to JPype class path
    if len(endpoints) > 0:
        endpoints = endpoints[:1] + sorted(endpoints[1:])
        _logger.debug('Using endpoints %s', endpoints)
        _, workspace = jgo.resolve_dependencies(
            '+'.join(endpoints),
            m2_repo=get_m2_repo(),
            cache_dir=get_cache_dir(),
            manage_dependencies=get_manage_deps(),
            repositories=repositories,
            verbose=get_verbose()
        )
        jpype.addClassPath(os.path.join(workspace, '*'))

    # Initialize JPype JVM
    jvm_options = _options

    # append any additional options
    if _add_options == '':
        pass
    else:
        jvm_options = jvm_options + ' ' + _add_options

    # store options used for the jvm in _options -- user can check what was used
    _options = jvm_options
    jpype.startJVM(jvm_options)

    return


def JVM_status():
    return jpype.isJVMStarted()

def maven_scijava_repository():
    """
    :return: url for public scijava maven repo
    """
    return 'https://maven.scijava.org/content/groups/public'

def add_endpoints(*endpoints):
    global _endpoints
    _logger.debug('Adding endpoints %s to %s', endpoints, _endpoints)
    _endpoints.extend(endpoints)

def get_endpoints():
    global _endpoints
    return _endpoints

def add_repositories(*args, **kwargs):
    global _repositories
    for arg in args:
        _logger.debug('Adding repositories %s to %s', arg, _repositories)
        _repositories.update(arg)
    _logger.debug('Adding repositories %s to %s', kwargs, _repositories)
    _repositories.update(kwargs)

def get_repositories():
    global _repositories
    return _repositories

def set_verbose(level):
    global _verbose
    _logger.debug('Setting verbose level to %d (was %d)', level, _verbose)
    _verbose = level


def get_verbose():
    global _verbose
    _logger.debug('Getting verbose level: %d', _verbose)
    return _verbose


def set_manage_deps(manage):
    global _manage_deps
    _logger.debug('Setting manage deps to %d (was %d)', manage, _manage_deps)
    _manage_deps = manage


def get_manage_deps():
    global _manage_deps
    return _manage_deps


def set_cache_dir(dir):
    global _cache_dir
    _logger.debug('Setting cache dir to %s (was %s)', dir, _cache_dir)
    _cache_dir = dir


def get_cache_dir():
    global _cache_dir
    return _cache_dir


def set_m2_repo(dir):
    global _m2_repo
    _logger.debug('Setting m2 repo dir to %s (was %s)', dir, _m2_repo)
    _m2_repo = dir


def get_m2_repo():
    global _m2_repo
    return _m2_repo

def add_classpath(*path):
    jpype.addClassPath(*path)


def set_classpath(*path):
    jpype.addClassPath(*path)


def get_classpath():
    return jpype.getClassPath()

def add_options(options):
    global _add_options
    _add_options = options

def get_options():
    global _options
    return _options

def set_options(options):
    global _options
    _options = options
