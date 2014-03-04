from distlib import util

base_project_url = 'https://www.red-dove.com/pypi/projects/'
base_project_url = 'http://projects.caniusepython3.com/'


def get_project_data(name):
    url = '%s%s/%s/project.json' % (base_project_url, name[0].upper(), name)
    return util._get_external_data(url)
util.get_project_data = get_project_data


def get_package_data(name, version):
    url = ('%s%s/%s/package-%s.json' % (base_project_url, name[0].upper(),
                                        name, version))
    return util._get_external_data(url)
util.get_package_data = get_package_data
