from inbox.log import get_logger
logger = get_logger()

from inbox.events.google import GoogleEventsProvider
from inbox.events.outlook import OutlookEventsProvider
from inbox.events.icloud import ICloudEventsProvider
from inbox.sync.base_sync import BaseSync
from inbox.models import Event
from inbox.util.debug import bind_context


__provider_map__ = {'gmail': GoogleEventsProvider,
                    'outlook': OutlookEventsProvider,
                    'icloud': ICloudEventsProvider}


class EventSync(BaseSync):
    """Per-account event sync engine.

    Parameters
    ----------
    account_id: int
        The ID for the user account for which to fetch event data.

    poll_frequency: int
        In seconds, the polling frequency for querying the events provider
        for updates.

    Attributes
    ---------
    log: logging.Logger
        Logging handler.
    """
    def __init__(self, provider_name, account_id, namespace_id,
                 poll_frequency=300):
        bind_context(self, 'eventsync', account_id)
        self.log = logger.new(account_id=account_id, component='event sync')
        self.log.info('Begin syncing Events...')

        BaseSync.__init__(self, account_id, namespace_id, poll_frequency, -2,
                          'Events', provider_name)

    @property
    def provider(self):
        return __provider_map__[self._provider_name]

    @property
    def target_obj(self):
        return Event

    def last_sync(self, account):
        return account.last_synced_events

    def set_last_sync(self, account, dt):
        account.last_synced_events = dt
