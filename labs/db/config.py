"""
Configuration file for database connections
"""

import os

get = lambda p, default: os.environ.get(p, default)

class MySQLConfig:
    """configuration for MySQL"""

    username    = get('MYSQL_USERNAME', 'root')
    password    = get('MYSQL_PASSWORD', 'root')
    host        = get('MYSQL_HOST', 'localhost')
    database    = get('MYSQL_DATABASE', 'ecosystem_mapping')


class MongoConfig:
    """configuration for MongoDB"""

    host        = get('MONGODB_HOST', "localhost")
    port        = get('MONGODB_PORT', 27017)
    database    = get('MONGODB_DATABASE', "ecosystem_mapping")
