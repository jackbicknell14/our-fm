import contextlib
from flask.views import http_method_funcs
import flask_restplus

MODELS_ATTR = '__method_models'


class ResourceAdder:

    def __init__(self, restplus_api):
        """An instance of a flask restplus api is required to register the models
        against.

        Args:
            restplus_api (flask_restplus.Api): instance of Api
        """
        self.api = restplus_api

    def add(self, namespace, resource, *urls, endpoint,):
        """Wrapper to create api resources, registering those which are not protected by
        jwt. Flask restplus models are also registered against the instance of the
        flask_restplus Api so they are correctly displayed in the swagger.

        Args:
            namespace(flask_restplus.Namespace): namespace to attach the resource to
            resource(flask_restplus.Resource): class to attach the resource to
            urls(str): url(s) to attach to the resource
            endpoint(str): internal name for the resource
        """
        self._register_models(resource)
        namespace.add_resource(resource, *urls, endpoint=endpoint)

    def _register_models(self, resource):
        """Iterates through all the possible http methods and looks for any models which
        need to be registered against the flask restplus Api instance.

        Args:
            resource (flask_restplus.Resource): class containing http methods to be
                registered against a url
        """
        for method in http_method_funcs:  # post, put, get etc
            try:
                resource_method = getattr(resource, method)  # eg Tiers.post
                models = getattr(resource_method, MODELS_ATTR)
            except AttributeError:
                continue  # method not implemented or no models

            self.api.models.update(models)

    def __repr__(self):
        return f'<ResourceAdder for api version {self.api.version}>'


class Api:
    """Wrapper around flask_restplus.Api to allow models to be identified and registered
    against multiple instances of flask_restplus.Api. This enables versioning, with each
    version having its own blueprint and namespaces, but able to re-use interfaces
    from previous versions, by simply importing them. If models used by 'expect' or
    'marshal_with' are not registered against the api the swagger documentaion does not
    work."""

    def __init__(self, restplus_api):
        """An instance of flask_restplus.Api is required just to be able to use its
        methods for applying the documentation decorators. Any flask_restplus.Api instance
        could actually be used as this step does not actually register the documentation
        against the instance, it just stores it in the method attribute __apidoc__.

        Args:
            restplus_api (flask_restplus.Api): instance of Api
        """
        self.api = restplus_api

    def model(self, *args, **kwargs):
        """Wrapper to instantiate a flask_restplus model. The argumants to this method
        are passed right on to create a Model.

        Returns:
            flask_restplus.Model: an instance of Model
        """
        return flask_restplus.Model(*args, **kwargs)

    def __getattr__(self, attr):
        """Wrapper around flask_restplus decorators. Calls are intercepted to enable
        models to be identified and stored in an attribute for later retrieval and
        registration against an instance of flask_restplus.Api
        """
        def decorator(*args, **kwargs):
            def wrapper(func):
                func_models = getattr(func, MODELS_ATTR, {})
                models = self._find_models(args)
                func_models.update(models)
                setattr(func, MODELS_ATTR, func_models)

                # manually apply the flask_restplus api decorator
                # eg: Tiers.post = api.expect(*args, **kwargs)(Tiers.post)
                api_attr = getattr(self.api, attr)
                func = api_attr(*args, **kwargs)(func)

                return func
            return wrapper
        return decorator

    def _find_models(self, args):
        """Wrapper to identify flask_restplus.Model in arguments supplied to a
        flask_restplus decorator. Nested models are located by the method recursively
        calling itself.

        Args:
            args (*): arguments to interrogate for flask_restplus.Models

        Returns:
            dict: models that have been found, keyed to their name: {model.name: model}
        """
        models = {}
        for arg in args:
            if isinstance(arg, flask_restplus.Model):
                models[arg.name] = arg

                nested_models = []
                for field in arg.values():
                    with contextlib.suppress(AttributeError):
                        # look for models nested in fields.List
                        field = getattr(field, 'container')

                    with contextlib.suppress(AttributeError):
                        # look for models nested in fields.Nested
                        nested_models.append(getattr(field, 'nested'))

                models.update(self._find_models(nested_models))

        return models

