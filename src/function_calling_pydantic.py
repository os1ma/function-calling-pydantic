import os

import openai
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    ingredient: str = Field(description="材料", examples=["鶏もも肉"])
    quantity: str = Field(description="分量", examples=["300g"])


class Recipe(BaseModel):
    ingredients: list[Ingredient]
    steps: list[str] = Field(description="手順", examples=[["材料を切ります。", "材料を炒めます。"]])


OUTPUT_RECIPE_FUNCTION = {
    "name": "output_recipe",
    "description": "レシピを出力する",
    "parameters": Recipe.model_json_schema(),
}


def main():
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "カレーのレシピを教えてください。"}],
        functions=[OUTPUT_RECIPE_FUNCTION],
        function_call={"name": OUTPUT_RECIPE_FUNCTION["name"]},
    )

    response_message = response["choices"][0]["message"]
    function_call_args = response_message["function_call"]["arguments"]

    recipe = Recipe.model_validate_json(function_call_args)
    print(type(recipe))
    print(recipe)


if __name__ == "__main__":
    main()
