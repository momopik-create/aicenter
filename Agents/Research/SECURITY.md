# Research Agent Security

## Secrets

The Research Agent must never store API keys in source code.

Required environment variables:

- SEARCH_PROVIDER
- TAVILY_API_KEY

Never commit:

- .env
- real API keys
- access tokens
- passwords
- private credentials
