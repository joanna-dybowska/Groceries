from modules.recipe_pdf_class import RecipePDF
from modules.groceries_class import Groceries
from datetime import datetime as dt
import os

# input file path
pdf_path = "results/2000-kcal-DIY-WYSOKOBIALKOWY.pdf"

# results file paths
folder_today = dt.today().strftime("%Y-%m-%d")
folder_results = f"results/{folder_today}"
if not os.path.exists(folder_results):
    os.makedirs(folder_results)

txt_path = f"{folder_results}/recipes.txt"
xlsx_path = f"{folder_results}/groceries.xlsx"

# STEP 1 - create TXT file with recipes
pages_numbers = [73, 79, 106, 137, 140] # [73, 79, 87, 106, 108, 109, 136, 137, 140]
recipe_pdf = RecipePDF(pdf_path, txt_path, pages_numbers)
recipe_pdf.correct_titles_user_input()
recipe_pdf.save_recipes_txt_file()

# OPTIONALLY: check recipes extracted and make some corrections and changes before running STEP 2!

# STEP 2 - create XLSX file with groceries
groceries = Groceries(txt_path, xlsx_path)
groceries.change_servings_user_input()
groceries.save_groceries_to_xlsx_file()