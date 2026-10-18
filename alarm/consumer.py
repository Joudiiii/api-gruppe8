from __future__ import annotations

import json
import time
import pika

def process_message(message: object):
    """Validate a sensor payload before processing it.
    Invalid or malformed messages should be rejected early instead of being processed with wrong assumptions
    """
    if not isinstance(message, dict):
        raise ValueError("Message must be a JSON object")
