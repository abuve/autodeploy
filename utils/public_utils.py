def business_node_top(obj, node_name=''):
    if obj.parent_unit:
        parent_name = business_node_top(obj.parent_unit, node_name)
        node_name = '%s-%s' % (parent_name, obj.name)
        return node_name
    else:
        return obj.name


def business_user_filter(obj, user_type):
    user_list = []
    for group_obj in getattr(obj, user_type).all():
        for user_obj in group_obj.users.all():
            user_list.append(user_obj.username)
    if user_list:
        return user_list
    else:
        if obj.parent_unit:
            return business_user_filter(obj.parent_unit, user_type)
        else:
            return user_list
