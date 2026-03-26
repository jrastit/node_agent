from __future__ import absolute_import, division, print_function

__metaclass__ = type

import logging
import json

from ansible.plugins.callback import CallbackBase

logger = logging.getLogger()


# Create a callback plugin so we can capture the output
class ResultsCollectorJSONCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in.

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin.
    """

    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_ok_history = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        host_name = host.get_name()
        self.host_ok[host_name] = result

        task_name = ""
        if getattr(result, "_task", None) is not None:
            task_name = result._task.get_name() or ""

        self.host_ok_history.setdefault(host_name, []).append(
            {
                "task": task_name,
                "result": result._result,
            }
        )
        # logger.info(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result
