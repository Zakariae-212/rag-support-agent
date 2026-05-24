import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rag import search


def test_rag_search():

    results = search(
        "Comment créer un compte ?"
    )

    assert len(results) > 0

    assert "text" in results[0]