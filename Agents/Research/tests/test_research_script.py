import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Agents.Research.review_store import ReviewStore


def main():
    # Verify the public input surface without contacting Tavily.
    import scripts.research as research

    with TemporaryDirectory() as temp:
        root = Path(temp)
        affiliates = root / "affiliates.json"
        affiliates.write_text(json.dumps({"vultr": "https://example.com"}), encoding="utf-8")
        original = research.AFFILIATES_FILE
        research.AFFILIATES_FILE = affiliates
        try:
            assert research.load_affiliates() == {"vultr": "https://example.com"}
            store = ReviewStore(directory=root / "reviews")
            live = root / "src/content/products"
            live.mkdir(parents=True)
            (live / "vultr.md").write_text("seed", encoding="utf-8")
            research.ROOT = root
            assert research.should_skip("vultr", store, False, False) is True
            assert research.should_skip("vultr", store, False, True) is False
            assert research.should_skip("vultr", store, True, False) is False
        finally:
            research.AFFILIATES_FILE = original

    print("Research script targeting test: PASSED")


if __name__ == "__main__":
    main()
