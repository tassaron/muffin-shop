# Modules for Muffin Shop

## In JSON

1. `blueprints`: A list of blueprints to be imported and registered on the Flask instance.
1. `root`: Name of the Python module containing the blueprint that **won't** have its routes prepended with the blueprint's name. Ordinarily, routes will have the blueprint prepended to the route. A blueprint being root means that _all_ routes in that blueprint will maintain their exact routes. **Note:** The `index_route` of this blueprint will be `/` if this blueprint is also root in the "main" module. _E.g._, shop blueprint is the root blueprint of the shop module, so shop.index becomes `/` if the shop blueprint is also root of the main module, else shop.index becomes `/shop`, but shop.allproducts is _always_ `/products` unless the shop blueprint isn't root of anything.
1. `index`: Endpoint of the index for this module. This is the endpoint which will be / if this module is the root module, otherwise the endpoint which will be linked to by the module's tab in the navbar.
1. `env`: List of critical environment variables which will be needed by the module. If these variables aren't set in production, the app won't start. In development a warning will be logged instead.
1. `ignore`: List of routes from this module which will be ignored; use to remove unused pages. _E.g._, if a shop doesn't need categories you may ignore `["shop.shop_category_index"]` (or just `shop_category_index` if shop is the root module).
1. `name`: The human-readable name of the module which might be displayed somewhere in a future version

## In Python

-   To create a new URL on the webapp, create a module by creating a Python package inside the `controllers` package. In this package, import Blueprint and use it like you would in any other Flask app. Edit the JSON to include the new Python package and name of the blueprint variable. **Note:** The name of the blueprint (passed in the constructor) will be pre-pended to the URL unless the module is defined as `root`

## In Jinja

1. HTML templates are in `config/templates` and site-specific overrides of templates should be in `config/client/<instance>/templates` (use `CONFIG_PATH` environment variable)
1. Markdown can be used for some text-heavy parts of the site. It goes in a `markdown` directory within the config path. Markdown is parsed into HTML before reaching the Jinja template, so you must [tell Jinja not to escape the HTML](https://flask.palletsprojects.com/en/1.1.x/templating/#controlling-autoescaping).
1. Currently the template directories are hardcoded on line 87 of `src/helpers/main/app_factory.py` so you have to edit that file to add a new directory. In future we might automatically determine the loader path based on module name.

### Identifying the currently selected navigation tab

-   In Jinja templates, use the `selected` variable for the current tab. This is a pretty minor detail so I'm just using unique numbers for whatever pages I want to be a page as I decide to add them.

1. about.about_page
2. shop.shop_product_list, shop.view_product
3. account.login, account.register, account.reset_password
4. arcade.arcade_index, arcade.game_page, arcade.token_leaderboard
5. about.bio_page
6. blog.blog_newest_posts