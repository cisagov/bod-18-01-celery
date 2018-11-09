# Broker settings
broker_url = 'redis://localhost:6379/1'

# Backend that stores task state and results
result_backend = 'redis://localhost:6379/1'

# Modules to import when the worker starts up
include = (
    'bod1801.tasks'
)

# Set some task parameters
task_annotations = {
    'bod1801.tasks.trustymail': {
        'rate_limit': '4/m'
    },
    'bod1801.tasks.sslyze': {
        'rate_limit': '4/m'
    }
}
