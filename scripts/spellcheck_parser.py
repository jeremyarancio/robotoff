from typing import Tuple
from tqdm import tqdm
from functools import partial
import requests

import pandas as pd
import typer

from robotoff import settings
from robotoff.types import ServerType, JSONType
from robotoff.utils import http_session


tqdm.pandas()

DATA_PATH = settings.PROJECT_DIR / "data/spellcheck/postprocessed_data.parquet"

app = typer.Typer()


@app.command()
def compute(
    sample_size: float = typer.Option(1.0, help="Sample size to parse"),
    random_state: int = typer.Option(42, help="Seed for the random sample"),
    data_path: str = typer.Option(DATA_PATH, help="Path to the data"),
    timeout: int = typer.Option(30, help="Timeout for the parser"),
) -> None:
    df = pd.read_parquet(data_path).sample(frac=sample_size, random_state=random_state)
    print(f"Number of products: {len(df)}")

    partial_fn = partial(apply_fn, timeout=timeout)

    df[
        ["ingredients_n", "before_unknown_ingredients_n", "after_unknown_ingredients_n"]
    ] = df.progress_apply(lambda row: (partial_fn(row)), axis=1, result_type="expand")

    df.to_parquet(DATA_PATH.parent / "saved_data.parquet")

    sum_before = df["before_unknown_ingredients_n"].sum()
    sum_after = df["after_unknown_ingredients_n"].sum()

    print(
        f"Before Spellcheck: {sum_before} unknwon ingredients\nAfter Spellcheck: {sum_after} unknown ingredients"
    )
    print(f"Spellcheck reduced {(sum_before - sum_after)/sum_before} unknown ingredients")


def compute_ingredients_n(
    text: str,
    lang: str,
    timeout: int,
) -> Tuple[int, int]:
    product = parse_ingredients(text, lang, timeout)
    return product["unknown_ingredients_n"], product["ingredients_n"]


def apply_fn(row, timeout: int) -> Tuple[int, int, int]:
    """Function used in the apply method of a pandas DataFrame."""
    original_text = row["text"]
    correction_text = row["correction"]
    lang = row["lang"]

    before_unknown_ingredients_n, ingredients_n = compute_ingredients_n(
        original_text, lang, timeout
    )
    after_unknown_ingredients_n, _ = compute_ingredients_n(
        correction_text, lang, timeout
    )
    return ingredients_n, before_unknown_ingredients_n, after_unknown_ingredients_n


def parse_ingredients(text: str, lang: str, timeout: int) -> JSONType:
    """Copied from robotoff.off.parse_ingredients and slighlty modified.
    """
    base_url = settings.BaseURLProvider.world(ServerType.off)
    # by using "test" as code, we don't save any information to database
    # This endpoint is specifically designed for testing purposes
    url = f"{base_url}/api/v3/product/test"

    if len(text) == 0:
        raise ValueError("text must be a non-empty string")

    try:
        r = http_session.patch(
            url,
            auth=settings._off_request_auth,
            json={
                "fields": "ingredients,ingredients_n,unknown_ingredients_n",
                "lc": lang,
                "tags_lc": lang,
                "product": {
                    "lang": lang,
                    f"ingredients_text_{lang}": text,
                },
            },
            timeout=timeout,
        )
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.SSLError,
        requests.exceptions.Timeout,
    ) as e:
        raise RuntimeError(
            f"Unable to parse ingredients: error during HTTP request: {e}"
        )

    if not r.ok:
        raise RuntimeError(
            f"Unable to parse ingredients (non-200 status code): {r.status_code}, {r.text}"
        )

    response_data = r.json()

    if response_data.get("status") != "success":
        raise RuntimeError(f"Unable to parse ingredients: {response_data}")

    return response_data.get("product", {})


if __name__ == "__main__":
    app()
