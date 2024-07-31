import os
import logging
import sentry_sdk
from omo_api.utils import get_env_var

logger = logging.getLogger()

def configure_apm() -> None:
    APM_PROVIDER = os.environ.get('APM_PROVIDER', None)

    if APM_PROVIDER == 'sentry':

        SENTRY_DSN = get_env_var('SENTRY_DSN')

        logger.info('Initializing APM: Sentry')
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )