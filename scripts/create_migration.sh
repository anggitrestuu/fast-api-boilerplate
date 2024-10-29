#!/bin/bash

# Check if message parameter is provided
if [ -z "\$1" ]; then
    echo "Usage: ./create_migration.sh 'migration message'"
    exit 1
fi

# Create migration
alembic revision --autogenerate -m "\$1"

# Show created migration files
echo "Created migration files:"
ls -l alembic/versions/*.py | tail -n 1