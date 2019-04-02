from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.oci.facade.facade import OracleFacade
from ScoutSuite.providers.oci.resources.utils import get_non_provider_id


class ApiKeys(Resources):

    def __init__(self, user, facade: OracleFacade):
        self.facade = facade
        self.user = user

    async def fetch_all(self, **kwargs):
        for raw_user_api_key in await self.facade.identity.get_user_api_keys(user_id=self.user['identifier']):
            id, api_key = self._parse_api_key(raw_user_api_key)
            self[id] = api_key

    def _parse_api_key(self, raw_api_key):
        api_key = {}
        api_key['id'] = get_non_provider_id(raw_api_key.key_id)
        api_key['identifier'] = raw_api_key.key_id
        api_key['fingerprint'] = raw_api_key.fingerprint
        api_key['state'] = raw_api_key.lifecycle_state

        return api_key['id'], api_key

