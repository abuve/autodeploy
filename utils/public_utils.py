def business_node_top(obj, node_name=''):
    if obj.parent_unit:
        parent_name = business_node_top(obj.parent_unit, node_name)
        node_name = '%s-%s' % (parent_name, obj.name)
        return node_name
    else:
        return obj.name


def business_node_low(obj, node_name=''):
    if obj.parent_level.all():
        child_list = []
        for child_obj in obj.parent_level.all():
            child_id = business_node_low(child_obj, node_name)
            child_list.append(child_id)
            node_id = '%s-%s' % (obj.id, '-'.join(i for i in child_list))
        return node_id
    else:
        return str(obj.id)


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
