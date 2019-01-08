#coding: utf-8
from ckan.controllers.home import HomeController
from ckan.controllers.api import ApiController
from ckan.common import c
import ckan.logic as logic
import ckan.model as model
import ckan.lib.base as base
from ckan.lib.base import request
import json
import ckan.plugins as p
from ckanext.googleanalytics.controller import GAApiController
import ckanext.gobar_theme.helpers as gobar_helpers

from pylons import response


class GobArHomeController(HomeController):
    def _list_groups(self):
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user or c.author
        }
        data_dict_page_results = {
            'all_fields': True,
            'type': 'group',
            'limit': None,
            'offset': 0,
        }
        return logic.get_action('group_list')(context, data_dict_page_results)

    def _featured_packages(self):
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user or c.author,
            'for_view': True
        }
        data_dict = {
            'q': ''
        }
        search = logic.get_action('package_search')(context, data_dict)
        if 'results' in search:
            results = search['results']
            featured_packages = []
            for result in results:
                for extra_pair in result['extras']:
                    if extra_pair['key'] == 'home_featured' and extra_pair['value'] == 'true':
                        featured_packages.append(result)

            segmented_packages = [featured_packages[n:n + 2] for n in range(len(featured_packages))[::2]]
            return segmented_packages
        return []

    def _packages_with_resource_type_equal_to_api(self):
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user or c.author
        }
        data_dict = {
            'query': 'resource_type:api',
            'limit': None,
            'offset': 0,
        }
        return logic.get_action('resource_search')(context, data_dict).get('results', [])

    def index(self):
        c.groups = self._list_groups()
        c.sorted_groups = sorted(c.groups, key=lambda x: x['display_name'].lower())
        c.featured_packages = self._featured_packages()
        return super(GobArHomeController, self).index()

    def about(self):
        return base.render('about.html')

    def about_ckan(self):
        return base.render('about_ckan.html')

    def apis(self):
        c.apis = self._packages_with_resource_type_equal_to_api()
        return base.render('apis/apis.html')

    def view_about_section(self, title_or_slug):
        sections = gobar_helpers.get_theme_config('about.sections', [])

        for section in sections:
            if section.get('slug', '') == title_or_slug or section['title'] == title_or_slug:
                # la variable `section` contiene la sección buscada
                break
        else:
            base.abort(404, u'Sección no encontrada')

        return base.render('section_view.html', extra_vars={'section': section})

    def super_theme_taxonomy(self):
        response.content_type = 'application/json; charset=UTF-8'
        return base.render('home/super_theme_taxonomy.html')

class GobArApiController(GAApiController, ApiController):

    def _remove_extra_id_field(self, json_string):
        json_dict = json.loads(json_string)
        has_extra_id = False
        if 'result' in json_dict and 'fields' in json_dict['result']:
            for field in json_dict['result']['fields']:
                if 'id' in field and field['id'] == '_id':
                    has_extra_id = True
                    json_dict['result']['fields'].remove(field)
            if has_extra_id and 'records' in json_dict['result']:
                for record in json_dict['result']['records']:
                    if '_id' in record:
                        del record['_id']
        return json.dumps(json_dict)

    def action(self, logic_function, ver=None):
        default_response = super(GobArApiController, self).action(logic_function, ver)
        if logic_function == 'datastore_search':
            default_response = self._remove_extra_id_field(default_response)
        return default_response

    def status(self):
        context = {'model': model, 'session': model.Session}
        data_dict = {}

        status = logic.get_action('status_show')(context, data_dict)
        gobar_status = logic.get_action('gobar_status_show')(context, data_dict)
        status['gobar_artifacts'] = gobar_status

        return self._finish_ok(status)