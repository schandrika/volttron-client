from volttron.client.vip.agent import build_agent

agent = build_agent()

agent.vip.pubsub.publish(peer="pubsub", topic="foo", message="bar").get(timeout=5)
