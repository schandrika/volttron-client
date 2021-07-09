import pytest

from volttron.client.vip.agent import Agent


def test_subsystems_available():
    agent = Agent()
    assert agent.vip.auth
    assert agent.vip.channel
    assert agent.vip.config
    assert agent.vip.health
    assert agent.vip.heartbeat
    assert agent.vip.hello
    assert agent.vip.peerlist
    assert agent.vip.ping
    assert agent.vip.pubsub
    assert agent.vip.rpc
    assert agent.vip.web
