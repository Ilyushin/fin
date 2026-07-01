"""Tests for provider interface conformance and selection."""

from app.market.interface import MarketDataProvider
from app.market.provider import create_provider
from app.market.simulator import Simulator
from app.market.massive import MassiveClient


def test_simulator_is_a_provider():
    assert isinstance(Simulator(), MarketDataProvider)


def test_massive_is_a_provider(monkeypatch):
    monkeypatch.setenv("MASSIVE_API_KEY", "test-key")
    assert isinstance(MassiveClient(tickers=["AAPL"]), MarketDataProvider)


def test_provider_defaults_to_simulator(monkeypatch):
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    assert isinstance(create_provider(), Simulator)


def test_provider_selects_massive_when_key_set(monkeypatch):
    monkeypatch.setenv("MASSIVE_API_KEY", "test-key")
    assert isinstance(create_provider(), MassiveClient)


def test_blank_api_key_falls_back_to_simulator(monkeypatch):
    monkeypatch.setenv("MASSIVE_API_KEY", "   ")
    assert isinstance(create_provider(), Simulator)
