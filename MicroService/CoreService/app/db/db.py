import os
config = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('HOST'),
                'port': os.getenv('PORT'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD'),
                'database': os.getenv('DATABASE'),
                'maxsize':'100'
            }
        },
    },
    'apps': {
        'models': {
            'models': ['__main__'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
}

