# coding=utf-8

from pysite.route_manager import RouteManager

manager = RouteManager()
app = manager.app

if __name__ == '__main__':
    manager.run()
