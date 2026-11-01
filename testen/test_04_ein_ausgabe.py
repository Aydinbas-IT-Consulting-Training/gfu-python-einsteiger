"""Teil 4: Eingabe und Ausgabe testen.

Auch Funktionen mit input() und print() lassen sich testen. Dafür bringt
pytest zwei eingebaute Fixtures mit:

- monkeypatch ersetzt während eines Tests eine Funktion durch eine andere,
  hier input() durch ein lambda mit einer festen Antwort. Nach dem Test ist
  das echte input() wieder da.
- capsys fängt alles auf, was print() ausgibt. capsys.readouterr().out
  liefert die bisherige Ausgabe als einen String.

Starten:  uv run pytest test_04_ein_ausgabe.py -v
"""

import pytest

from prices import ask_net_price, print_receipt

# --- Eingabe ersetzen: monkeypatch -------------------------------------------


def test_ask_net_price_reads_comma(monkeypatch):
    # "builtins.input" ist der volle Name von input(). Die Funktion wird mit dem
    # Text "Nettopreis: " aufgerufen, deshalb braucht das lambda den Parameter
    # prompt, auch wenn es ihn nicht benutzt.
    monkeypatch.setattr("builtins.input", lambda prompt: "3,50")
    assert ask_net_price() == 3.5


def test_ask_net_price_rejects_text(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "gratis")
    with pytest.raises(ValueError):
        ask_net_price()


# --- Sprechende Namen für Fälle: pytest.param ---------------------------------
# pytest.param(..., id="komma") gibt einem Fall von parametrize einen Namen.
# pytest -v zeigt dann test_ask_net_price_formats[komma] statt der Werte.


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        pytest.param("3,50", 3.5, id="komma"),
        pytest.param("3.50", 3.5, id="punkt"),
        pytest.param("12", 12.0, id="ganze-zahl"),
        pytest.param(" 4,20 ", 4.2, id="leerzeichen"),
    ],
)
def test_ask_net_price_formats(monkeypatch, answer, expected):
    monkeypatch.setattr("builtins.input", lambda prompt: answer)
    assert ask_net_price() == expected


# --- Ausgabe auffangen: capsys -----------------------------------------------


def test_print_receipt(cart, capsys):
    cart.add("Kaffee", 3.50)
    cart.add("Wasser", 2.00)
    print_receipt(cart)
    output = capsys.readouterr().out  # alles, was print() geschrieben hat
    assert output.splitlines() == [
        "Kaffee: 4.17 €",
        "Wasser: 2.38 €",
        "Summe: 6.55 €",
    ]
