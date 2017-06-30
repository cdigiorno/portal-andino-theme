# coding=utf-8
import re
import pkg_resources
import os
from codecs import open
from os import path


def gobar_status_show(context, data_dict):
    artifacts = []
    plugins = ['ckanext-harvest', 'ckanext-gobar-theme', 'ckanext-hierarchy']
    for plugin in plugins:
        version = _get_plugin_version(plugin)
        artifact = {plugin: version}
        artifacts.append(artifact)
    portal_andino_version = _get_portal_andino_version()
    artifacts.append(portal_andino_version)
    return artifacts


def _get_plugin_version(plugin):
    try:
        version = pkg_resources.require(plugin)[0].version
    except:
        version = None
    return version


def _get_portal_andino_version():
    os.chdir('/')
    portal_dir = path.abspath(path.join(os.getcwd(), 'portal/'))
    try:
        with open(path.join(portal_dir, 'version')) as file:
            version = file.read()
            version = re.sub('[^\d\.]', '', version)
    except:
        version = None
    return {'portal-andino': version}