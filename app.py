# coding=utf-8

from os import environ

from pysite.route_manager import RouteManager

manager = RouteManager()
app = manager.app

debug = environ.get('DEBUG', "0")
if debug == "1":
    print('good times')
    app.jinja_env.auto_reload = True

if __name__ == '__main__':
    manager.run()
