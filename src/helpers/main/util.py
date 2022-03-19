def generic_url_for(rule):
    try:
        generic_url = url_for(
            rule.endpoint, **{arg_name: 1 for arg_name in rule.arguments}
        )
    except BuildError:
        generic_url = rule.endpoint
    return generic_url


@lru_cache
def all_urls():
    return [
        generic_url_for(rule)
        for rule in current_app.url_map.iter_rules()
        if "static" not in rule.endpoint and "GET" in rule.methods
    ]


@lru_cache
def all_base_urls():
    return [
        url_for(rule.endpoint)
        for rule in current_app.url_map.iter_rules()
        if len(rule.arguments) == 0 and "GET" in rule.methods
    ]