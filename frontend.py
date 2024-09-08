import gradio as gr
import matplotlib.pyplot as plt
import base64
from processImage import nutrition_values, nutrition_pie_chart, mirco_nutrition_values, get_sugar_images, get_calorie_burn_info
import json

# Static nutrition data (simulating LLM output)
NUTRITION_DATA = {
    "calories": 200,
    "total_fat": 8,
    "saturated_fat": 1,
    "trans_fat": 0,
    "cholesterol": 0,
    "sodium": 160,
    "total_carbohydrate": 37,
    "dietary_fiber": 4,
    "total_sugars": 12,
    "protein": 3,
    "vitamin_d": 2,
    "calcium": 260,
    "iron": 8,
    "potassium": 235
}

def create_micronutrient_chart(data):
    nutrients = ['Vitamin D', 'Calcium', 'Iron', 'Potassium']
    values = [data['vitamin_d'], data['calcium'], data['iron'], data['potassium']]

    fig, ax = plt.subplots()
    ax.bar(nutrients, values)
    plt.title("Micronutrient Content")
    plt.ylabel("Amount")
    return fig

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def update_dashboard(image):
    if image is None:
        error_html = """
        <div style="background-color: #ffcccc; padding: 15px; border-radius: 5px; text-align: center;">
            <h3 style="color: #cc0000;">Error: No Image Uploaded</h3>
            <p>Please upload an image of a nutrition label before clicking 'Analyze'.</p>
        </div>
        """
        return error_html, None, None
    
    image_base64 = image_to_base64(image)

    data = nutrition_values(image_base64)

    data = json.loads(data)
    allergens = ", ".join(data["nutritionFacts"].get("allergens", [])) or "No allergens detected."

    print("---------------")
    print(data)
    print("---------------")

    
    # Create charts
    macro_chart = nutrition_pie_chart(data)
    micro_data = mirco_nutrition_values(data)
    micro_chart = create_micronutrient_chart(NUTRITION_DATA)
    sugar_image_fig = get_sugar_images(data)
    calorie_burn_fig = get_calorie_burn_info(data)

    return  macro_chart, micro_chart, sugar_image_fig, calorie_burn_fig, allergens

with gr.Blocks() as demo:
    gr.Markdown("# Ose Busters")
    gr.Markdown("Upload an image of a nutrition label and click 'Analyze' to see the nutritional information displayed as a dashboard with charts.")
    
    with gr.Row():
        image_input = gr.Image(type="filepath", label="Upload Nutrition Label Image",  height=300, width=300)
    
    with gr.Row():
        submit_button = gr.Button("Analyze")
    
    with gr.Row():
        with gr.Column(scale=2):
            macro_chart_output = gr.Plot(label="Macronutrient Distribution")
            micro_chart_output = gr.Plot(label="Micronutrient Content")

        with gr.Column(scale=2):
            sugar_image_output = gr.Plot(label="Sugar Cube Representation")
            calorie_burn_output = gr.Plot(label="Calorie Burning Equivalents")
            allergen_output = gr.Textbox(label="Detected Allergens", lines=4)
    
    submit_button.click(
        fn=update_dashboard,
        inputs=[image_input],
        outputs=[macro_chart_output, micro_chart_output, sugar_image_output, calorie_burn_output, allergen_output]
    )

demo.launch(share=True)