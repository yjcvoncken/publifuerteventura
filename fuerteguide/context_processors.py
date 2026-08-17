def language_navigation(request):
    path = request.path
    parts = path.lstrip("/").split("/", 1)
    suffix = "/" + parts[1] if parts[0] in {"es", "it"} and len(parts) > 1 else path
    if not suffix or suffix == "/es" or suffix == "/it":
        suffix = "/"
    return {"language_paths": {"en": suffix, "es": "/es" + suffix, "it": "/it" + suffix}}
