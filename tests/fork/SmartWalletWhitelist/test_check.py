import brownie
import pytest


BAD_CHECKER = """pragma solidity 0.5.17;

contract SmartWalletChecker {
    function check(address) external view { return; }
}
"""

CHECKER = """pragma solidity 0.5.17;

contract SmartWalletChecker {
    bool response;
    function setResponse(bool _response) external { response = _response; }
    function check(address) external view returns (bool) { return response; }
}
"""


@pytest.fixture(scope="module")
def checker(accounts):
    Checker = brownie.compile_source(CHECKER).SmartWalletChecker
    yield Checker.deploy({'from': accounts[0]})


@pytest.fixture(scope="module")
def bad_checker(accounts):
    Checker = brownie.compile_source(BAD_CHECKER).SmartWalletChecker
    yield Checker.deploy({'from': accounts[0]})


def test_checker_approves(accounts, agent, whitelist, checker):
    whitelist.commitSetChecker(checker, {'from': agent})
    whitelist.applySetChecker({'from': agent})

    checker.setResponse(True, {'from': agent})

    assert whitelist.check(accounts[0]) is True


def test_checker_no_approval(accounts, agent, whitelist, checker):
    whitelist.commitSetChecker(checker, {'from': agent})
    whitelist.applySetChecker({'from': agent})

    checker.setResponse(False, {'from': agent})

    assert whitelist.check(accounts[0]) is False


def test_bad_checker_raises(accounts, agent, whitelist, bad_checker):
    whitelist.commitSetChecker(bad_checker, {'from': agent})
    whitelist.applySetChecker({'from': agent})

    with brownie.reverts():
        whitelist.check(accounts[0])


def test_EOA_as_checker_raises(accounts, agent, whitelist):
    whitelist.commitSetChecker(accounts[0], {'from': agent})
    whitelist.applySetChecker({'from': agent})

    with brownie.reverts():
        whitelist.check(accounts[0])


def test_whitelisted_no_checker(accounts, agent, whitelist):
    whitelist.approveWallet(accounts[0], {'from': agent})

    assert whitelist.check(accounts[0]) is True


def test_not_whitelisted_no_checker(accounts, agent, whitelist):
    assert whitelist.check(accounts[0]) is False


def test_whitelisted_checker_returns_false(accounts, agent, checker, whitelist):
    whitelist.approveWallet(accounts[0], {'from': agent})

    whitelist.commitSetChecker(checker, {'from': agent})
    whitelist.applySetChecker({'from': agent})
    checker.setResponse(False, {'from': agent})

    # whitelist should take priority over checker
    assert whitelist.check(accounts[0]) is True
