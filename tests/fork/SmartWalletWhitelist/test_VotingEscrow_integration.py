import brownie

MONTH = 86400 * 30
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def test_initial_assumptions(chain, token, voter, voting_escrow, whitelist):
    assert voting_escrow.smart_wallet_checker() == whitelist
    assert whitelist.check(voter) is True
    assert token.balanceOf(voter) > 0


def test_create_lock(chain, token, voter, voter_owner):
    balance = token.balanceOf(voter)
    voter.createLock(balance, chain.time() + MONTH, {'from': voter_owner})


def test_increase_amount(chain, token, voter, voter_owner):
    balance = token.balanceOf(voter)
    voter.createLock(balance // 2, chain.time() + MONTH, {'from': voter_owner})
    voter.increaseAmount(balance // 2, {'from': voter_owner})


def test_withdraw(chain, token, voter, voter_owner):
    balance = token.balanceOf(voter)
    voter.createLock(balance, chain.time() + MONTH, {'from': voter_owner})
    chain.sleep(MONTH)
    voter.release({'from': voter_owner})


def test_withdraw_no_checker(chain, agent, token, voter, voter_owner, voting_escrow, whitelist):
    balance = token.balanceOf(voter)
    voter.createLock(balance, chain.time() + MONTH, {'from': voter_owner})

    voting_escrow.commit_smart_wallet_checker(ZERO_ADDRESS, {'from': agent})
    voting_escrow.apply_smart_wallet_checker({'from': agent})
    chain.sleep(MONTH)

    # `voter` should be able to withdraw even if the whitelist contract is removed
    voter.release({'from': voter_owner})
    assert token.balanceOf(voter) == balance


def test_create_lock_no_checker(chain, agent, voter, voter_owner, voting_escrow, whitelist):
    voting_escrow.commit_smart_wallet_checker(ZERO_ADDRESS, {'from': agent})
    voting_escrow.apply_smart_wallet_checker({'from': agent})

    with brownie.reverts("Smart contract depositors not allowed"):
        voter.createLock(1, chain.time() + MONTH, {'from': voter_owner})
