from ckanext.gobar_theme_base.controller import GobArHomeController as HomeController
from ckanext.gobar_theme_base.controller import GobArApiController as ApiController
from ckanext.gobar_theme_base.controller import GobArUserController as UserController
import ckan.lib.helpers as h
from ckan.common import c, request
import ckan.logic as logic
import ckan.model as model
import ckan.lib.base as base
import ckan.plugins as p


class GobArHomeController(HomeController):
    def about(self):
        return base.render('about.html')


class GobArApiController(ApiController):
    def status(self):
        context = {'model': model, 'session': model.Session}
        data_dict = {}

        status = logic.get_action('status_show')(context, data_dict)
        gobar_status = logic.get_action('gobar_status_show')(context, data_dict)
        status['gobar_artifacts'] = gobar_status

        return self._finish_ok(status)


class GobArUserController(UserController):
    def login(self, error=None):
        # Do any plugin login stuff
        for item in p.PluginImplementations(p.IAuthenticator):
            item.login()

        if 'error' in request.params:
            h.flash_error(request.params['error'])

        if not c.user:
            came_from = request.params.get('came_from')
            if not came_from:
                came_from = h.url_for(controller='user', action='logged_in',
                                      __ckan_no_root=True)
            c.login_handler = h.url_for(
                self._get_repoze_handler('login_handler_path'),
                came_from=came_from)
            if error:
                vars = {'error_summary': {'': error}}
            else:
                vars = {}
            return base.render('user/login.html', extra_vars=vars)
        else:
            return h.redirect_to('home')