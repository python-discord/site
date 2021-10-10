# Static Builds
This directory includes all the needed information to build and deploy static previews of the site.

Static deployments use [django-distill](https://github.com/meeb/django-distill) to build the static content.
The content is built in GitHub Actions, and is fetched and deployed by Netlify.


## Instructions
These are the configuration instructions to get started with static deployments.
They are split into two parts:

- [Building The Site](#building-the-site)
- [Deploying To Netlify](#deploying-to-netlify)


### Building The Site
To get started with building, you can use the following command:

```shell
python -m pip install httpx==0.19.0
python manage.py distill-local build --traceback --force --collectstatic
```

Alternatively, you can use the [Dockerfile](/Dockerfile) and extract the build.

Both output their builds to a `build/` directory.

> Warning: If you are modifying the [build script](./netlify_build.py), make sure it is compatible with Python 3.8.


### Deploying To Netlify
To deploy to netlify, link your site GitHub repository to a netlify site, and use the following settings:

Build Command:
`python -m pip install httpx==0.19.0 && python static-builds/netlify_build.py`

Publish Directory:
`build`

Environment Variables:
- PYTHON_VERSION: 3.8
- TOKEN: A GitHub token with access to download build artifacts.


Note that at this time, if you are deploying to netlify yourself, you won't have access to the
fa-icons pack we are using, which will lead to many missing icons on your preview.
You can either update the pack to one which will work on your domain, or you'll have to live with the missing icons.
