import brownie


def test_initial_assumptions(accounts, whitelist, voter):
    assert whitelist.wallets(accounts[0]) is False
    assert whitelist.wallets(voter) is True


def test_approve_wallet(accounts, agent, whitelist):
    whitelist.approveWallet(accounts[0], {'from': agent})

    assert whitelist.wallets(accounts[0]) is True


def test_approve_and_revoke(accounts, agent, whitelist):
    whitelist.approveWallet(accounts[0], {'from': agent})
    whitelist.revokeWallet(accounts[0], {'from': agent})

    assert whitelist.wallets(accounts[0]) is False


def test_approve_already_approved(accounts, agent, whitelist):
    whitelist.approveWallet(accounts[0], {'from': agent})
    whitelist.approveWallet(accounts[0], {'from': agent})

    assert whitelist.wallets(accounts[0]) is True


def test_revoke_wallet(agent, voter, whitelist):
    whitelist.revokeWallet(voter, {'from': agent})

    assert whitelist.wallets(voter) is False


def test_commit_only_owner(accounts, whitelist):
    with brownie.reverts("!dao"):
        whitelist.approveWallet(accounts[0], {'from': accounts[0]})


def test_apply_only_owner(accounts, whitelist):
    with brownie.reverts("!dao"):
        whitelist.revokeWallet(accounts[0], {'from': accounts[0]})


def test_approve_event(accounts, agent, whitelist):
    tx = whitelist.approveWallet(accounts[0], {'from': agent})

    assert tx.events['ApproveWallet'].values() == [accounts[0]]
