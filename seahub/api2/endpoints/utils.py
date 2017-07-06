# Copyright (c) 2012-2016 Seafile Ltd.
import logging

from rest_framework import status

import seaserv
from pysearpc import SearpcError

from seahub.api2.utils import api_error
from seahub.base.templatetags.seahub_tags import email2nickname, \
        email2contact_email

logger = logging.getLogger(__name__)

def api_check_group(func):
    """
    Decorator for check if group valid
    """
    def _decorated(view, request, group_id, *args, **kwargs):
        group_id = int(group_id) # Checked by URL Conf
        try:
            group = seaserv.get_group(group_id)
        except SearpcError as e:
            logger.error(e)
            error_msg = 'Internal Server Error'
            return api_error(status.HTTP_500_INTERNAL_SERVER_ERROR, error_msg)

        if not group:
            error_msg = 'Group %d not found.' % group_id
            return api_error(status.HTTP_404_NOT_FOUND, error_msg)

        return func(view, request, group_id, *args, **kwargs)

    return _decorated

def get_user_contact_email_dict(email_list):
    email_list = set(email_list)
    user_contact_email_dict = {}
    for email in email_list:
        if not user_contact_email_dict.has_key(email):
            user_contact_email_dict[email] = email2contact_email(email)

    return user_contact_email_dict

def get_user_name_dict(email_list):
    email_list = set(email_list)
    user_name_dict = {}
    for email in email_list:
        if not user_name_dict.has_key(email):
            user_name_dict[email] = email2nickname(email)

    return user_name_dict
