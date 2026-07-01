"""Tests for parsing the Massive (Polygon.io) snapshot response."""

from app.market.massive import parse_snapshot


def test_parses_ticker_and_price():
    data = {"tickers": [{"ticker": "AAPL", "lastTrade": {"p": 190.5}}]}
    assert parse_snapshot(data) == [("AAPL", 190.5)]


def test_parses_multiple_tickers():
    data = {
        "tickers": [
            {"ticker": "AAPL", "lastTrade": {"p": 190.5}},
            {"ticker": "GOOGL", "lastTrade": {"p": 175.0}},
        ]
    }
    assert parse_snapshot(data) == [("AAPL", 190.5), ("GOOGL", 175.0)]


def test_skips_items_missing_price():
    data = {"tickers": [{"ticker": "AAPL", "lastTrade": {}}]}
    assert parse_snapshot(data) == []


def test_skips_items_missing_ticker():
    data = {"tickers": [{"lastTrade": {"p": 190.5}}]}
    assert parse_snapshot(data) == []


def test_empty_response_yields_empty_list():
    assert parse_snapshot({}) == []
    assert parse_snapshot({"tickers": []}) == []


def test_price_is_coerced_to_float():
    data = {"tickers": [{"ticker": "AAPL", "lastTrade": {"p": 190}}]}
    result = parse_snapshot(data)
    assert result == [("AAPL", 190.0)]
    assert isinstance(result[0][1], float)
