import logging

# Default
DEBUG = False
TESTING = False
DATABASE_URI = 'postgres://postgres:docker@127.0.0.1:5432/providentia'
LOGGING_LEVEL = logging.INFO

# Example prod
# DEBUG = False
# DATABASE_URI = 'postgres://USERNAME:PASSWORD@www.providentia.com:PORT/providentia'
# SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
# CORS_ORIGINS = ["http://www.providentia.com:4200"]

# Example dev
# DEBUG = True
# SECRET_KEY = 'dev'
# CORS_ORIGINS = ["http://localhost:4200"]
# DATABASE_URI = 'postgres://postgres:docker@127.0.0.1:5432/providentia'
# LOGGING_LEVEL = logging.DEBUG

# Config for databases to benchmark
# POSTGRES_YELP_CONN = 'postgres://postgres:docker@127.0.0.1:5432/yelp'
# JANUSGRAPH_YELP_CONN = 'ws://localhost:8182/gremlin'
# CASSANDRA_YELP_CONN = 'todo'

# Example testing
# TESTING = True

