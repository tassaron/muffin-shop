# Modules for Tassaron's Flask Template
A description of the keys in a module's definition.

1. `name`: The human-readable name of the module which will be displayed on the tab that navigates to this module's index
1. `blueprints`: A list of blueprints to be imported and registered on the Flask instance.
1. `root`: Name of the Python module containing the blueprint that **won't** have its routes prepended with the blueprint's name *if this module is the root module*. (Ordinarily, routes belonging to blueprints will have the name of the blueprint prepended to the route.)
1. `index`: Endpoint of the index for this module. This is the endpoint which will be / if this module is the root module, otherwise the endpoint which will be linked to by the module's tab in the navbar.
1. `env`: List of critical environment variables which will be needed by the module. If these variables aren't set in production, the app won't start. In development a warning will be logged instead.
1. `profile_models`: SQLAlchemy database models which will be displayed as a tab in the user's profile. They should be placed in the main app's `models.py`.
1. `model_views`: Views to be embedded in the tab in the user's profile. This view will receive an instance of the corresponding model to be displayed, which could be None if the user does not have a record for that model.
1. `model_forms`: Views to be embedded in the edit form of the user's profile when editing the corresponding model, if applicable to the model. **Not implemented yet.**