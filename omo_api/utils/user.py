from fastapi.encoders import jsonable_encoder
from omo_api.config import config
from omo_api.db.models import User
from omo_api.utils.vector_store import get_active_vector_store

def get_user_ctx(user: User) -> dict:
    user_dict = jsonable_encoder(user)
    installed_apps_dict = get_installed_connectors(user)
    vecstore_config_dict = get_vector_store_config(user)

    user_ctx = {}
    user_ctx.update(user_dict)
    user_ctx.update(installed_apps_dict)
    user_ctx.update(vecstore_config_dict)

    return user_ctx


def get_installed_connectors(user: User) -> dict:
    installed_connectors = {
        'connectors': []
    }
    for app in config['connectors']:
        app_configs = getattr(user.team, f"{app}_configs", None)
        # user has existing configs i.e. it's installed
        if not app_configs:
            continue

        installed_connectors['connectors'].append({ 'name': app, 'id': [app_config.id for app_config in app_configs]})

    return installed_connectors

def get_vector_store_config(user: User) -> dict:
    config = {}
    vecstore = get_active_vector_store()['name']
    keys = ['id', 'index_name', 'environment', 'namespaces', 'created_at', 'updated_at']
    config['vector_store'] = {key: "" for key in keys}
    config['vector_store']['provider'] = vecstore

    vecstore_config = getattr(user.team, f"{vecstore}_configs")[0]
    for key in keys:
        config['vector_store'][key] = getattr(vecstore_config, key)

    return config