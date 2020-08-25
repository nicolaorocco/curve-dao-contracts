import pytest


@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    pass


@pytest.fixture(scope="session")
def agent(accounts):
    yield accounts.at("0x40907540d8a6C65c637785e8f8B742ae6b0b9968")


@pytest.fixture(scope="session")
def voter_owner(accounts):
    yield accounts.at("0x2D407dDb06311396fE14D4b49da5F0471447d45C")


@pytest.fixture(scope="module")
def binance(accounts):
    yield accounts.at("0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE")


@pytest.fixture(scope="module")
def whitelist(SmartWalletWhitelist):
    yield SmartWalletWhitelist.at("0xca719728Ef172d0961768581fdF35CB116e0B7a4")


@pytest.fixture(scope="module")
def voting_escrow(VotingEscrow, whitelist, agent):
    escrow = VotingEscrow.at("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2")
    escrow.commit_smart_wallet_checker(whitelist, {'from': agent})
    escrow.apply_smart_wallet_checker({'from': agent})
    yield escrow


@pytest.fixture(scope="module")
def voter(Contract, binance, token):
    yearn_voter = Contract.from_explorer("0xF147b8125d2ef93FB6965Db97D6746952a133934")
    token.transfer(yearn_voter, token.balanceOf(binance), {'from': binance})
    yield yearn_voter


@pytest.fixture(scope="module")
def token(ERC20CRV):
    yield ERC20CRV.at("0xD533a949740bb3306d119CC777fa900bA034cd52")
