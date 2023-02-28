import logging
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
# from axes.signals import log_user_login_failed as axes_log_user_login_failed

# from axes.signals import log_user_login_failed
logger = logging.getLogger('django.server')


@receiver(user_logged_in)
def online_user_logged_in(sender, request, user, **kwargs):
    logger.debug('user {} logged in through ip {} page {}'.format(user, request.META['REMOTE_ADDR'], request.META.get('HTTP_REFERER')))
    user.is_online = True
    user.save()


@receiver(user_logged_out)
def offline_user_logged_out(sender, request, user, **kwargs):
    user.is_online = False
    user.save()
    try:
        user.auth_token.delete()
    except:
        pass


# user_login_failed.disconnect(axes_log_user_login_failed)
