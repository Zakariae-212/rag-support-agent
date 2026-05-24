import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database_faq import search_faq


def test_search_faq_found():

    result = search_faq(
        "Quels sont les moyens de paiement ?"
    )

    assert result is not None


def test_search_faq_not_found():

    result = search_faq(
        "Question inexistante"
    )

    assert result is None