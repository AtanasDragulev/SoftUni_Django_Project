def get_attribute_filters(attributes):
    attribute_groups = {}
    for attribute in attributes:
        name = attribute.name
        value = attribute.value
        if name not in attribute_groups:
            attribute_groups[name] = []
        if value not in attribute_groups[name]:
            attribute_groups[name].append(value)
    for group, items in attribute_groups.items():
        items.sort()

    return attribute_groups
