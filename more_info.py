# Addtional Information

# Steps

# Show Sugar Cubes
from PIL import Image
import matplotlib.pyplot as plt

total_sugars=int(nutrition_data['Total Sugars'].rstrip('g'))
print("Total Sugars",total_sugars)

sugar_img_path="/content/Sugar.jpg"
half_sugar_path="/content/Sugar_half.jpg"


total_sugars=int(nutrition_data['Total Sugars'].rstrip('g'))
print("Total Sugars",total_sugars)
sugar_grams=26.2
cube_grams=4
whole_cubes=int(sugar_grams//cube_grams)

#Half cube is either 0 or 1
half_cubes=int(round(sugar_grams%cube_grams / cube_grams))
print("Whole Cubes", whole_cubes)
print("Half Cubes", half_cubes)

# Loop for whole cubes.
# How do we make the images side by side?
for i in range(whole_cubes):
  img = Image.open(sugar_img_path)
  plt.imshow(img)
  plt.axis('off')  # Hide the axis labels
  plt.show()

# If statement for half cubes
if half_cubes > 0:
  img = Image.open(half_sugar_path)
  plt.imshow(img)
  plt.axis('off')  # Hide the axis labels
  plt.show()

# ********** Steps ***************
total_calories=nutrition_data['Calories']
print("")
print("To burn",total_calories, "calories")
print("You need to walk",total_calories * 25,"Steps")




