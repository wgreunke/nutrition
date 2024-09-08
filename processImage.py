import os
from dotenv import load_dotenv
from PIL import Image

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
import matplotlib.pyplot as plt
import boto3

from prompt import prompt

# Load environment variables from .env file
load_dotenv()

# Access environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')


bedrock_client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0},
    client=bedrock_client,
)

def nutrition_values(image_data):
    message = HumanMessage(
    content=[
        {"type": "text", "text": prompt},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
    ],
    )
    response = llm.invoke([message])

    return response.content

def mirco_nutrition_values(data):

    vitamin_d = 0
    calcium = 0
    iron = 0
    potassium = 0

    if 'nutrients' in data['nutritionFacts']:
        for nutrient in data['nutritionFacts']['nutrients']:
            name = nutrient.get('name', '').lower()
            amount = nutrient.get('amount', '0g').lower()
            try:
                amount_value = float(amount[:-1])
            except ValueError:
                amount_value = 0

            
            if 'calcium' in name:
                calcium = amount_value
            elif 'iron' in name:
                iron = amount_value
            elif 'potassium' in name:
                potassium= amount_value
            elif 'vitamin d' in name or 'carb' in name:
                vitamin_d = amount_value

    micro_nutrition = {
    "vitamin_d": vitamin_d,
    "calcium": calcium,
    "iron": iron,
    "potassium": potassium
    }

    print(micro_nutrition)

    return micro_nutrition


def get_calorie_burn_info(data):
    calories = 0
    if 'nutritionFacts' in data:
        calories = data['nutritionFacts'].get('calories', 0)

    # Calculate steps as calories * 25
    steps = calories * 25

    # Adjust the size of the calorie burn chart (set to be bigger)
    fig, ax = plt.subplots(figsize=(3, 3))  # Adjusted figure size
    ax.axis('off')

    # Add text about calories and step equivalent
    ax.text(0.5, 0.9, f"Calories: {calories}", ha='center', va='center', 
            transform=ax.transAxes, fontsize=16, fontweight='bold')

    ax.text(0.5, 0.5, f"Equivalent to {steps} steps", ha='center', va='center', 
            transform=ax.transAxes, fontsize=14)

    # Set the title
    ax.set_title("Calorie Burning Equivalents in Steps", fontsize=16, fontweight='bold', pad=20)

    # Adjust layout
    plt.tight_layout()

    return fig

import matplotlib.pyplot as plt
from PIL import Image

def get_sugar_images(data):
    total_sugars = 0
    # Extract sugar value from the nutrient data
    if 'nutrients' in data['nutritionFacts']:
        for nutrient in data['nutritionFacts']['nutrients']:
            name = nutrient.get('name', '').lower()
            amount = nutrient.get('amount', '0g').lower()
            try:
                amount_value = float(amount[:-1])
            except ValueError:
                amount_value = 0
            
            if 'sugar' in name:
                total_sugars = amount_value
                break

    # Calculate the number of sugar cubes (assuming 1 sugar cube = 4 grams of sugar)
    sugar_img_path = "sugar.png"
    half_sugar_path = "sugar_half.png"
    cube_grams = 4
    whole_cubes = int(total_sugars // cube_grams)
    half_cubes = int(round(total_sugars % cube_grams / cube_grams))

    # Set up the figure for displaying sugar cubes
    total_cubes = whole_cubes + half_cubes
    spacing = 0.1  # Adjust this value to set the space between cubes
    fig_width = max(total_cubes * (1 + spacing), 3)  # Ensure minimum width
    fig, ax = plt.subplots(figsize=(fig_width, 2))

    # Remove axis
    ax.axis('off')

    # Iterate over whole cubes and plot them one at a time with spaces in between
    for i in range(whole_cubes):
        img = Image.open(sugar_img_path)
        ax.imshow(img, aspect='auto', extent=(i * (1 + spacing), i * (1 + spacing) + 1, 0, 1))

    # Add half cube if necessary, placing it after the whole cubes
    if half_cubes > 0:
        img = Image.open(half_sugar_path)
        ax.imshow(img, aspect='auto', extent=(whole_cubes * (1 + spacing), whole_cubes * (1 + spacing) + 1, 0, 1))

    # Add text to show the exact sugar value
    ax.text(0.5, -0.3, f'{total_sugars}g sugar', ha='center', va='center', 
            transform=ax.transAxes, fontsize=12, fontweight='bold')
    
    # Set the title
    ax.set_title("Sugar Content", fontsize=14, fontweight='bold', pad=10)

    # Adjust the plot limits to fit all cubes
    ax.set_xlim(0, total_cubes * (1 + spacing))
    ax.set_ylim(-0.5, 1.5)

    # Adjust layout to prevent clipping of the text
    plt.tight_layout()

    # Return the figure
    return fig

def nutrition_pie_chart(data):
    total_fat = 0
    dietary_fiber = 0
    total_sugars = 0
    protein = 0
    total_starch = 0
    total_carbohydrate = 0
    serving_size = 0
    
    # Extract serving information (if needed)
    if 'nutritionFacts' in data:
        # Extract serving size
        serving_info = data['nutritionFacts'].get('servingInfo', {})
        serving_size_str = serving_info.get('servingSize', '0g')
        try:
            serving_size = float(serving_size_str[:-1])  # Assuming 'g' is the unit for serving size
        except ValueError:
            serving_size = 0

        if 'nutrients' in data['nutritionFacts']:
            for nutrient in data['nutritionFacts']['nutrients']:
                name = nutrient.get('name', '').lower()
                amount = nutrient.get('amount', '0g').lower()
                try:
                    amount_value = int(amount[:-1])
                except ValueError:
                    amount_value = 0
                
                if 'fat' in name and 'total' in name:
                    total_fat = amount_value
                elif 'fiber' in name:
                    dietary_fiber = amount_value
                elif 'sugar' in name:
                    total_sugars = amount_value
                elif 'protein' in name:
                    protein = amount_value
                elif 'carbohydrate' in name or 'carb' in name:
                    total_carbohydrate = amount_value

            # Calculate Total Starch (Total Carbohydrate - Fiber - Sugars)
            
            total_starch = total_carbohydrate - dietary_fiber - total_sugars

    # Calculate "Other" (Serving Size - Total Fat - Total Carbohydrate - Protein)
    other = max(0, serving_size - total_fat - total_carbohydrate - protein)

    labels = ['Total Fat', 'Fiber', 'Total Sugars', 'Total Starch', 'Protein', 'Other']
    sizes = [max(0, total_fat), max(0, dietary_fiber), max(0, total_sugars), max(0, total_starch), max(0, protein), other]

    colors = {
        'Total Fat': '#ffcc99',  # Light orange
        'Fiber': '#99cc99',      # Light green
        'Total Sugars': '#FF0000',  # Red for sugar
        'Total Starch': '#66b3ff',  # Light blue
        'Protein': '#008000',    # green
        'Other': '#ffccff'       # Pink
    }


    filtered_labels = [label for label, size in zip(labels, sizes) if size > 0]
    filtered_sizes = [size for size in sizes if size > 0]

    filtered_colors = [colors[label] for label in filtered_labels]

    # Create pie chart
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=140,  colors=filtered_colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Display the chart
    ax.set_title("Nutrition Breakdown")
   
    return fig