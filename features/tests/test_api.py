try:
    from features import app as lexicode_app
except ImportError:
    import app as lexicode_app

import pytest


@pytest.fixture()
def client(tmp_path):
    lexicode_app.DB = str(tmp_path / 'test_progress.db')
    lexicode_app.init_db()
    lexicode_app.app.config['TESTING'] = True

    with lexicode_app.app.test_client() as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['ok'] is True
    assert data['app'] == 'LexiCode'


def test_words_endpoint_returns_cards(client):
    response = client.get('/api/words?mod=cs')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert {'word', 'tr', 'mod', 'progress'}.issubset(data[0].keys())


def test_settings_roundtrip(client):
    response = client.post('/api/settings', json={
        'daily_goal': '12',
        'active_mod': 'daily',
        'focus_mode': '1',
    })
    assert response.status_code == 200

    response = client.get('/api/settings')
    data = response.get_json()
    assert data['daily_goal'] == 12
    assert data['active_mod'] == 'daily'
    assert data['focus_mode'] is True


def test_tts_requires_text(client):
    response = client.post('/api/tts', json={'text': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False
    assert data['error'] == 'text_required'
