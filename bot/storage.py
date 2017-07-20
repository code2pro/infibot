import redis

class EphemeralStore(object):
    def __init__(self, ns, prefix, expire=180, db=0):
        self._redis = redis.Redis(host='localhost', port=6379, db=db)
        self._pipe = self._redis.pipeline()
        self._ns = ns
        self._prefix = prefix
        self._expire = expire

    def __contains__(self, key):
        return self.hgetall(key) is not None

    def __getitem__(self, key):
        return self.hgetall(key)

    def __setitem__(self, key, val):
        return self.hmset(key, val)

    def __delitem__(self, key):
        ikey = self.internalize_key(key)
        self._redis.delete(ikey)

    def internalize_key(self, key):
        return '{}.{}{}'.format(self._ns, self._prefix, key)

    def contains(self, key):
        ikey = self.internalize_key(key)
        ttl = self._redis.ttl(ikey)
        if ttl is None or ttl < 1:
            return None
        return True

    def hmset(self, key, dict_val):
        ikey = self.internalize_key(key)
        results = self._pipe.hmset(ikey, dict_val).expire(ikey, self._expire).execute()
        output = True
        for res in results:
            output = output and res
        return output

    def hgetall(self, key):
        ikey = self.internalize_key(key)
        if not self.contains(key):
            return None
        return self._redis.hgetall(ikey)
