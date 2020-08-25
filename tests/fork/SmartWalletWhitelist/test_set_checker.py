import brownie

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def test_initial_assumptions(whitelist):
    assert whitelist.checker() == ZERO_ADDRESS
    assert whitelist.future_checker() == ZERO_ADDRESS


def test_commit_set_checker(accounts, agent, whitelist):
    whitelist.commitSetChecker(accounts[0], {'from': agent})

    # only future whitelist should have changed
    assert whitelist.future_checker() == accounts[0]
    assert whitelist.checker() == ZERO_ADDRESS


def test_apply_set_checker(accounts, agent, whitelist):
    whitelist.commitSetChecker(accounts[0], {'from': agent})
    whitelist.applySetChecker({'from': agent})

    # only whitelist should have changed
    assert whitelist.future_checker() == accounts[0]
    assert whitelist.checker() == accounts[0]


def test_apply_without_commit(accounts, agent, whitelist):
    whitelist.applySetChecker({'from': agent})

    # call should succeed without effect
    assert whitelist.future_checker() == ZERO_ADDRESS
    assert whitelist.checker() == ZERO_ADDRESS


def test_commit_and_apply_twice(accounts, agent, whitelist):
    whitelist.commitSetChecker(accounts[0], {'from': agent})
    whitelist.applySetChecker({'from': agent})
    whitelist.applySetChecker({'from': agent})

    # call should succeed without effect
    assert whitelist.future_checker() == accounts[0]
    assert whitelist.checker() == accounts[0]


def test_commit_only_owner(accounts, whitelist):
    with brownie.reverts("!dao"):
        whitelist.commitSetChecker(accounts[0], {'from': accounts[0]})


def test_apply_only_owner(accounts, whitelist):
    with brownie.reverts("!dao"):
        whitelist.applySetChecker({'from': accounts[0]})
