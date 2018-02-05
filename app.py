#!/usr/bin/env python3.6

# Stdlib
from importlib.util import module_from_spec, spec_from_file_location
import mimetypes
import os

# External Libraries
from flask import Flask
from werkzeug.wrappers import Response

app = Flask()


def static_file(path: str):  # type: (str) -> (req: {Response}) -> Coroutine
    async def inner(req):  # type: ({Response}) -> Coroutine
        with open(path) as file:
            return Response(
                response=file.read(), mimetype=mimetypes.guess_type(path)[0])

    return inner


def find_static_files(dir_: str) -> list:  # type: (str) -> List[str]
    data = []
    for path, _, files in os.walk(dir_):
        if not files:
            continue

        for file in files:
            if not file.split(".")[-1] not in ("html", "css", "js"):
                continue

            pathname = f"{path[len(dir_):]}/{file.strip()}"
            data.append(pathname.split(".")[0], static_file(pathname))

    return data


def find_routes(
        dir_: str) -> list:  # type: (str) -> List[Tuple[str, str, callable]]
    data = []
    for path, _, files in os.walk(dir_):
        if not files:
            continue

        for file in files:
            if not file.endswith(".py"):
                continue
            pathname = f"{path}/{file.strip()}"
            spec = spec_from_file_location(file[:-3], pathname)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

            if not hasattr(module, "Index"):
                raise Exception("No `Index` class!")

            res = module.Index()
            del module, spec

            route_paths = res.path
            for path_ in route_paths:
                # TODO: Add all request types here
                for method in ("GET", "POST", "DELETE", "PATCH"):
                    if hasattr(res, method.lower()):
                        data.append((path_, method, getattr(
                            res, method.lower())))

    return data


def find_errors(dir_: str) -> list:  # type: (str) -> List[str]
    data = []
    for path, _, files in os.walk(dir_):
        if not files:
            continue

        for file in files:
            if not file.endswith(".py"):
                continue
            pathname = f"{path}/{file.strip()}"
            spec = spec_from_file_location(file[:-3], pathname)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

            if not hasattr(module, "Index"):
                raise Exception("No `Index` class!")

            res = module.Index()
            del module, spec
            data.append((res.error_code, res.err))

    return data


routes = find_routes("routes")
static = find_static_files("static")
errors = find_errors("error_handlers")

for path, method, handle in routes:
    app.add_url_rule(path, path, handle, method=method)

for path, handle in static:
    app.add_url_rule(path, path, handle, method="GET")

for errcode, handler in errors:
    app.register_error_handler(errcode, handler)

app.run(port=80)
