# Copyright (c) 2018 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
"""Contains logic for working with flow related information stored in the signac config."""
from signac.common import config

from ..errors import ConfigKeyError

_FLOW_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "import_packaged_environments": {"type": "boolean"},
        "status_performance_warn_threshold": {"type": "number"},
        "show_traceback": {"type": "boolean"},
        "eligible_jobs_max_lines": {"type": "integer"},
        "status_parallelization": {"type": "string"},
    },
}

_FLOW_CONFIG_DEFAULTS = {
    "import_packaged_environments": True,
    "status_performance_warn_threshold": 0.2,
    "show_traceback": False,
    "eligible_jobs_max_lines": 10,
    "status_parallelization": "none",
}


class _GetConfigValueNoneType:
    pass


_GET_CONFIG_VALUE_NONE = _GetConfigValueNoneType()


def require_config_value(key, ns=None, default=_GET_CONFIG_VALUE_NONE):
    """Request a value from the user's configuration, failing if not available.

    Parameters
    ----------
    key : str
        The environment specific configuration key.
    ns : str
        The namespace in which to look for the key. (Default value = None)
    default
        A default value in case the key cannot be found
        within the user's configuration.

    Returns
    -------
    object
        The value or default value.

    Raises
    ------
    :class:`~.ConfigKeyError`
        If the key is not in the user's configuration
        and no default value is provided.

    """
    try:
        if ns is None:
            return config.load_config()["flow"][key]
        else:
            return config.load_config()["flow"][ns][key]
    except KeyError:
        if default is _GET_CONFIG_VALUE_NONE:
            k = str(key) if ns is None else f"{ns}.{key}"
            raise ConfigKeyError("flow." + k)
        else:
            return default


def get_config_value(key, ns=None, default=None):
    """Request a value from the user's configuration.

    Parameters
    ----------
    key : str
        The configuration key.
    ns : str
        The namespace in which to look for the key. (Default value = None)
    default
        A default value returned if the key cannot be found within the user
        configuration.

    Returns
    -------
    object
        The value if found, None if not found.

    """
    return require_config_value(key=key, ns=ns, default=default)
