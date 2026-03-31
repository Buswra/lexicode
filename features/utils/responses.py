"""Standard JSON response helpers."""
from __future__ import annotations

from flask import jsonify


def api_success(data=None, status: int = 200, **extra):
    payload = {'ok': True}
    if isinstance(data, dict):
        payload.update(data)
    elif data is not None:
        payload['data'] = data
    payload.update(extra)
    return jsonify(payload), status


def api_error(error: str, message: str, status: int = 400, **extra):
    payload = {'ok': False, 'error': error, 'message': message}
    payload.update(extra)
    return jsonify(payload), status
