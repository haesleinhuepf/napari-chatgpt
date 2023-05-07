def search_functions(query:str):
    """
    Search for installed napari functions managed by the napari assistant.
    """
    import napari_assistant as na
    query = query.lower()

    text = []
    for name, function in na._categories.all_operations().items():
        docstring = "  " + function.__doc__.split("Parameters")[0]
        element = f"\n* {name}:\n{docstring}"
        if query in element.lower():
            text.append(element)

    return "".join(text)


