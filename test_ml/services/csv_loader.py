import pandas as pd
import ast
from typing import List, Dict
from schemas import Cocktail


class CSVLoaderService:
    def load_cocktails_from_csv(
            self,
            csv_path: str
    ) -> List[Dict]:
        df = pd.read_csv(
            csv_path,
            index_col=0
        )
        cocktails = []
        for _, row in df.iterrows():
            combined_text = str(
                row['text']
            )
            try:
                ingredients = ast.literal_eval(
                    row['ingredients']
                )
                if not isinstance(
                        ingredients,
                        list
                ):
                    ingredients = [str(
                        ingredients
                    )]
            except Exception:
                ingredients = [s.strip() for s in row['ingredients'].split(
                    ","
                )]
            cocktails.append(
                {
                    "id": int(
                        row["id"]
                    ),
                    "name": row["name"],
                    "alcoholic": row["alcoholic"],
                    "category": row["category"],
                    "glassType": row["glassType"],
                    "instructions": row["instructions"],
                    "ingredients": ingredients,
                    "text": combined_text
                }
            )
        return cocktails
