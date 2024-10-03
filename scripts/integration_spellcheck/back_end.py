from typing import Dict, Tuple
import requests

from .utils import diff_texts


BASE_URL = "https://robotoff.openfoodfacts.org/api/v1/"


def next_annotation() -> Tuple[str, str, str]:
    insight = import_random_insight()
    return insight["id"], insight["data"]["original"], insight["data"]["correction"]


def submit_correction(insight_id: str, original: str, correction: str) -> Tuple[str, str, str]:
    return next_annotation()


def import_random_insight(
    insight_type: str = "ingredient_spellcheck",
    count: int = 1,
    predictor: str = "fine-tuned-mistral-7b",
) -> Dict:
    """_summary_

    Args:
        insight_type (str, optional): _description_. Defaults to "ingredient_spellcheck".
        count (int, optional): _description_. Defaults to 1.
        predictor (str, optional): _description_. Defaults to "fine-tuned-mistral-7b".
    """
    url = f"{BASE_URL}/insights/random?count={count}&type={insight_type}&predictor={predictor}"
    response = requests.get(url)
    data = response.json()
    insight = data["insights"][0]
    return insight


def submit_to_product_opener(
    insight_id: str,
    skipped: bool,
    update: int = 0,
) -> None:
    url = f"{BASE_URL}/insights/annotate"
    annotation = -1 if skipped else 1
    data = {
        "insight_id": insight_id,
        "annotation": annotation,
        "update": update,
    }
    requests.post(url, data=data)
