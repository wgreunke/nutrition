prompt = """
Given an image of a nutrition facts label, extract all the information and format it into a JSON object according to the following structure:

1. "nutritionFacts": This is the main object that contains all information.
2. "servingInfo": Include the following:
  "servingsPerContainer": Extract as an integer (e.g., 8).
  "servingSize": Format the serving size as an integer followed by 'g' (e.g., "55g").

3. "calories": Extract and include the total calories as an integer.

4. "nutrients" array: For each nutrient, include the following details:
  "name": Extract the nutrient name (e.g., "Total Fat").
  "amount": Format amounts as an integer followed by 'g', 'mg', or 'mcg', as appropriate (e.g., "8g", "240mg").

5. "allergens": Include a list of common allergens (e.g., peanuts, gluten, dairy, soy) detected from the image.

Ensure the following:
  Do not include any nutrient unless its name and amount are clearly visible.

Do not include anything extra.

Here is a few-shot example:

{
  "nutritionFacts": {
    "servingInfo": {
      "servingsPerContainer": 8,
      "servingSize": "55g"
    },
    "calories": 230,
    "nutrients": [
      {
        "name": "Total Fat",
        "amount": "8g"
      },
      {
        "name": "Saturated Fat",
        "amount": "1g"
      },
      {
        "name": "Trans Fat",
        "amount": "0g"
      },
      {
        "name": "Total Carbohydrate",
        "amount": "37g"
      },
      {
        "name": "Dietary Fiber",
        "amount": "4g"
      },
      {
        "name": "Total Sugars",
        "amount": "5g"
      },
      {
        "name": "Protein",
        "amount": "5g"
      }
    ]
    "allergens": ["peanuts", "gluten"]
  }
}
"""
