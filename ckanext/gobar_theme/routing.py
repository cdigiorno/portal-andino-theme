from routes.mapper import SubMapper


class GobArRouter:

    def __init__(self, route_map, base_theme):
        self.route_map = route_map
        self.base_theme = base_theme.GobArRouter(route_map)

        self.home_controller = 'ckanext.gobar_theme.controller:GobArHomeController'
        self.config_controller = 'ckanext.gobar_theme.config_controller:GobArConfigController'
        self.api_controller = 'ckanext.gobar_theme.controller:GobArApiController'
        self.user_controller = 'ckanext.gobar_theme.controller:GobArUserController'

    def set_routes(self):
        self.connect_template_config()

    def connect_static(self):
        self.route_map.connect('gobar_about', '/acerca', action='about', controller=self.home_controller)
        self.base_theme.redirect(
            ('/about', '/acerca')
        )

    def connect_users(self):
        self.route_map.connect('login', '/ingresar', action='login', controller=self.user_controller)

    def connect_api(self):
        with SubMapper(self.route_map, controller=self.api_controller, path_prefix='/api{ver:/3|}', ver='/3') as m:
           m.connect('/util/status', action='status')

    def connect_template_config(self):
        with SubMapper(self.route_map, controller=self.config_controller) as m:
           m.connect('/configurar/titulo', action='edit_title')
           m.connect('/configurar/portada', action='edit_home')
           m.connect('/configurar/encabezado', action='edit_header')
           m.connect('/configurar/temas', action='edit_groups')
           m.connect('/configurar/redes', action='edit_social')
           m.connect('/configurar/pie-de-pagina', action='edit_footer')
           m.connect('/configurar/datasets', action='edit_datasets')
           m.connect('/configurar/organizaciones', action='edit_organizations')
           m.connect('/configurar/acerca', action='edit_about')
           m.connect('/configurar/metadata/google_fb', action='edit_metadata_google_fb')
           m.connect('/configurar/metadata/tw', action='edit_metadata_tw')
           m.connect('/configurar/mensaje_de_bienvenida', action='edit_greetings')

        self.base_theme.redirect(
           ('/configurar', '/configurar/titulo'),
           ('/configurar', '/configurar/metadata')
        )
