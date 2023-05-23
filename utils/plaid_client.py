import plaid
from plaid.api import plaid_api
from django.conf import settings

PLAID_CLIENT_ID = settings.PLAID_CLIENT_ID
PLAID_SECRET = settings.PLAID_SECRET
PLAID_PUBLIC_KEY = settings.PLAID_PUBLIC_KEY
PLAID_ENV = settings.PLAID_ENV

# Available environments are
# 'Production'
# 'Development'
# 'Sandbox'
def create_client():
    configuration = plaid.Configuration (
        host = plaid.Environment.Sandbox,
        api_key = {
            'clientId': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
        }
    )

    api_client = plaid.ApiClient (configuration)
    return plaid_api.PlaidApi (api_client)
