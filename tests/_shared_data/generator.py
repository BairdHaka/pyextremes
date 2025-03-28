from typing import Any, Dict

import pandas as pd

from pyextremes import get_extremes


def main() -> None:
    data = (
        pd.read_csv("battery_wl.csv", index_col=0, parse_dates=True)
        .squeeze()
        .sort_index(ascending=True)
        .dropna()
    )
    data = data.loc[data.index.year >= 1925]
    data = (
        data
        - (data.index.array - pd.to_datetime("1992"))
        / pd.to_timedelta("365.2425D")
        * 2.87e-3
    )
    kwargs: Dict[str, Any]
    for method in ["BM", "POT"]:
        for extremes_type in ["high", "low"]:
            if method == "BM":
                kwargs = {"block_size": "365.2425D", "errors": "ignore"}
            else:
                if extremes_type == "high":
                    kwargs = {"threshold": 1.35, "r": "24h"}
                else:
                    kwargs = {"threshold": -1.55, "r": "24h"}
            extremes = get_extremes(
                ts=data, method=method, extremes_type=extremes_type, **kwargs
            )
            extremes.round(2).to_csv(f"extremes_{method.lower()}_{extremes_type}.csv")


if __name__ == "__main__":
    main()
