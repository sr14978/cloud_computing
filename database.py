
from google.cloud import datastore

def get_client():
    return datastore.Client('cloudcomputingcompiler')

def update(data, id=None):
    client = get_client()
    if id:
        key = client.key('User', int(id))
    else:
        key = client.key('User')

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['executables'])

    entity.update(data)
    client.put(entity)


create = update
    
def create_user(user):
    if not 'executables' in user:
        user['executables'] = []
    create(user)
    print("created new user: ", user);

def update_user(user):
    id = get_user(user['user_id']).key.id
    update(user, id)

def get_user(user_id):

    query = get_client().query(kind='User')
    query.add_filter('user_id', '=', user_id)
    fetch = query.fetch(1)
    results = list(fetch)
    if len(results) == 0:
        return None
    else:
        return results[0]
        
def add_executable(user_id, executable):
    existing = get_user(user_id)
    if 'executables' in existing:
        executables = existing['executables']
    else:
        executables = []
    executables.append(executable)
    user = {
      'user_id': user_id,
      'name': existing['name'],
      'executables': executables
    }
    update(user, existing.key.id)