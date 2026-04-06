from modules.recipe_pdf_class import RecipePDF
from modules.groceries_class import Groceries

'''
This code reads recipes from PDF file (based on "Wysokobiałkowy wegański jadłospis DIY" by Irena Owsiak) to a TXT file.
Then from recipes from TXT file an XLSX file is created with ingredients to buy.
Optionally, the program asks user for corrections on recipes titles.
The program asks user for an input on number of servings for each recipe.
'''
# input file path
pdf_path = "results/2000-kcal-DIY-WYSOKOBIALKOWY.pdf"

# results file paths
txt_path = "results/4/recipes.txt"
xlsx_path = "results/4/groceries.xlsx"

# STEP 1 - create TXT file with recipes
pages_numbers = [86, 93, 128] # [73, 79, 87, 106, 108, 109, 136, 140, 147]
recipe_pdf = RecipePDF(pdf_path, txt_path, pages_numbers)
recipe_pdf.correct_titles_user_input()
recipe_pdf.save_recipes_txt_file()

# OPTIONALLY: check recipes extracted and make some corrections and changes before running STEP 2!

# STEP 2 - create XLSX file with groceries
groceries = Groceries(txt_path, xlsx_path)
groceries.change_servings_user_input()
groceries.save_groceries_to_xlsx_file()