# coding=utf-8

from os import environ

from pysite.route_manager import RouteManager

manager = RouteManager()
app = manager.app

debug = environ.get('TEMPLATES_AUTO_RELOAD', "no")
if debug == "yes":
    app.jinja_env.auto_reload = True

if __name__ == '__main__':
    manager.run()
