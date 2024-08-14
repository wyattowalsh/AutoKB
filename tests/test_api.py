import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from api import app

client = TestClient(app)

@pytest.fixture
def websocket():
    with client.websocket_connect("/ws") as websocket:
        yield websocket

def test_websocket_connection(websocket):
    assert websocket.application_state == 1  # WebSocketState.CONNECTED

def test_configuration_update(websocket):
    config_update = {"agent": {"description_max_words": 500}}
    websocket.send_text(yaml.dump(config_update))
    response = websocket.receive_text()
    assert "Configuration updated" in response

def test_streaming_progress_results(websocket):
    config_update = {"agent": {"description_max_words": 500}}
    websocket.send_text(yaml.dump(config_update))
    response = websocket.receive_text()
    assert "Configuration updated" in response

    result = websocket.receive_text()
    assert "Result sent" in result

def test_websocket_disconnect():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws") as websocket:
            websocket.close()
