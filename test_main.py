import hashlib
import math
import pytest

from crypto import CryptoSystem
from gacha import GachaSystem
import main as main_module

# Rolls chosen so make_hash_for_roll() always lands in a known tier
GUARANTEED_COMMON_ROLL = 9999
GUARANTEED_LEGENDARY_ROLL = 0


# Creating a fake hash for the target roll
def make_hash_for_roll(target_roll):
    lower_bound = math.ceil(target_roll * (2**32) / 10000)
    hex_prefix = format(lower_bound, '08x')
    return hex_prefix + "0" * 56


@pytest.fixture
def crypto():
    return CryptoSystem()


@pytest.fixture
def gacha():
    return GachaSystem()


@pytest.fixture
def seed_and_commitment(crypto):
    """A real seed and its matching commitment -- shared setup for both
    verify_commitment tests below."""
    seed = crypto.generate_server_seed()
    commitment = crypto.generate_hashed_server_seed(seed)
    return seed, commitment


@pytest.fixture
def blank_client_seed_input(monkeypatch):
    """Auto-answers the client seed prompt with blank input, so run_session()
    doesn't block on a real input() call during tests."""
    monkeypatch.setattr("builtins.input", lambda _: "")


#CRYPTO UNIT TESTS
def test_server_seed_is_32_bytes(crypto):
    seed = crypto.generate_server_seed()
    assert len(seed) == 64
    bytes.fromhex(seed)  # raises a ValueError if invalid characters are in the seed


def test_commitment_matches_known_seed(crypto):
    seed = "a" * 64
    expected = hashlib.sha256(seed.encode()).hexdigest()
    assert crypto.generate_hashed_server_seed(seed) == expected


def test_final_hash_is_deterministic(crypto):
    seed, client, nonce = "b" * 64, "clientseed", 5
    h1 = crypto.generate_final_hash(seed, client, nonce)
    h2 = crypto.generate_final_hash(seed, client, nonce)
    assert h1 == h2


def test_final_hash_changes_with_nonce(crypto):
    seed, client = "c" * 64, "clientseed"
    h1 = crypto.generate_final_hash(seed, client, nonce=1)
    h2 = crypto.generate_final_hash(seed, client, nonce=2)
    assert h1 != h2


def test_verify_commitment_succeeds_when_untampered(crypto, seed_and_commitment):
    seed, commitment = seed_and_commitment
    assert crypto.verify_commitment(seed, commitment) is True


def test_verify_commitment_fails_when_tampered(crypto, seed_and_commitment):
    _, commitment = seed_and_commitment
    tampered_seed = crypto.generate_server_seed()
    assert crypto.verify_commitment(tampered_seed, commitment) is False


##GACHA

def test_tier_boundaries(gacha):
    cases = {0: "Legendary", 99: "Legendary",
             100: "Rare", 2599: "Rare",
             2600: "Common", 9999: "Common"}
    for roll, expected_tier in cases.items():
        h = make_hash_for_roll(roll)
        tier, _, pity_triggered, _ = gacha.rarity_outcome(h, legendary_pity_counter=0)
        assert tier == expected_tier, f"roll {roll} -> got {tier}, expected {expected_tier}"
        assert pity_triggered is False


def test_pity_counter_increments_on_non_legendary(gacha):
    h = make_hash_for_roll(GUARANTEED_COMMON_ROLL)
    _, _, _, counter = gacha.rarity_outcome(h, legendary_pity_counter=5)
    assert counter == 6


def test_pity_counter_resets_on_natural_legendary(gacha):
    h = make_hash_for_roll(GUARANTEED_LEGENDARY_ROLL)
    _, _, _, counter = gacha.rarity_outcome(h, legendary_pity_counter=40)
    assert counter == 0


def test_hard_pity_forces_legendary_regardless_of_roll(gacha):
    h = make_hash_for_roll(GUARANTEED_COMMON_ROLL)
    hard_pity_limit = gacha.get_hard_pity()
    tier, _, pity_triggered, counter = gacha.rarity_outcome(h, legendary_pity_counter=hard_pity_limit - 1)
    assert tier == "Legendary"
    assert pity_triggered is True
    assert counter == 0


def test_hard_pity_does_not_fire_one_pull_early(gacha):
    h = make_hash_for_roll(GUARANTEED_COMMON_ROLL)
    hard_pity_limit = gacha.get_hard_pity()
    tier, _, pity_triggered, _ = gacha.rarity_outcome(h, legendary_pity_counter=hard_pity_limit - 2)
    assert tier == "Common"
    assert pity_triggered is False


##MAIN.PY INTEGRATION TESTS

def test_run_session_produces_valid_pulls(blank_client_seed_input):
    session = main_module.GameSession()
    server_seed, commitment, results, verified = session.run_session(num_pulls=25)

    assert len(results) == 25
    for r in results:
        assert 0 <= r["roll"] <= 9999
        assert r["tier"] in {"Legendary", "Rare", "Common"}
        assert isinstance(r["pity_triggered"], bool)
    assert verified is True


def test_hard_pity_guarantees_legendary_within_90_real_pulls(blank_client_seed_input):
    session = main_module.GameSession()
    _, _, results, verified = session.run_session(num_pulls=90)

    tiers = [r["tier"] for r in results]
    assert "Legendary" in tiers, "expected at least one legendary within 90 pulls due to hard pity"
    assert verified is True