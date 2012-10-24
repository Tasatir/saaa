from google.appengine.api import memcache
from google.appengine.ext import db
import random

"""
Esta clase es de proposito general.
	Crea Contadores fragmentados al vuelo solo asignandoles un nombre.
"""


class GeneralCounterShardConfig(db.Model):
    """Mantiene un alista de el numero de fragmentos d ecada contador."""
    name = db.StringProperty(required=True)
    num_shards = db.IntegerProperty(required=True, default=20)


class GeneralCounterShard(db.Model):
    """Fragmentos para cada contador"""
    name = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)


def get_count(name):
    """Regresa le valor de algun contador

    Parametros:
      name - El nombre del contador
    """
    total = memcache.get(name)
    if total is None:
        total = 0
        for counter in GeneralCounterShard.all().filter('name = ', name):
            total += counter.count
        memcache.add(name, total, 60)
    return total


def increment(name):
    """Incrementa el contador de el contador dado.
    Parametros:
      name - El nombre del contador
    """
    config = GeneralCounterShardConfig.get_or_insert(name, name=name)
    def txn():
        index = random.randint(0, config.num_shards - 1)
        shard_name = name + str(index)
        counter = GeneralCounterShard.get_by_key_name(shard_name)
        if counter is None:
            counter = GeneralCounterShard(key_name=shard_name, name=name)
        counter.count += 1
        counter.put()
    db.run_in_transaction(txn)
    # No hace nada si el contador no existe
    memcache.incr(name)


def increase_shards(name, num):
    """Incrementa el numero de fragmentos de algun contador.
    Nunca decrementara el numero de fragmentos.

    Parametros:
      name - EL nombre del contador
      num - Cuantos shards se usaran

    """
    config = GeneralCounterShardConfig.get_or_insert(name, name=name)
    def txn():
        if config.num_shards < num:
            config.num_shards = num
            config.put()
    db.run_in_transaction(txn)
