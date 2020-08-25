
def test_owner_is_dao(agent, whitelist):
    assert whitelist.dao() == agent
