import os
import pandas as pd
# openpyxl

class Groceries:
    def __init__(self, txt_file_path, xlsx_file_path):
        """Reads recipes and creates groceries pandas.DataFrame"""
        self.txt_file_path = txt_file_path
        self.xlsx_file_path = xlsx_file_path
        f = open(txt_file_path, encoding="utf-8")
        recipes_file = f.read()
        f.close()

        recipes_file = recipes_file.replace("–", "-")
        recipes_lists = recipes_file.split("\n\n")

        # get recipes and ingredients
        recipes_names_list = []
        servings_amount_list = []
        ingredients_list = []
        recipe_name = None
        servings = None
        self.recipe_servings_dict = {}
        for recipe in recipes_lists:
            for item in recipe.split("\n"):
                if "•" in item:
                    ingredients_list.append(item)
                    recipes_names_list.append(recipe_name)
                    servings_amount_list.append(servings)
                elif item:
                    # get recipe name and number of servings
                    recipe_name = item.split("-")[0].strip()
                    servings = int(item.split("-")[-1].strip()) # take character after last "-"
                    self.recipe_servings_dict[recipe_name] = servings

        ingredient_names_list = [i
                                 .replace("• ", "")
                                 .replace("•	 ", "")
                                 .replace("•	", "")
                                 .split("-")[0]
                                 .strip() for i in ingredients_list]
        ingredient_amounts_list = [i.split("-")[1].strip() for i in ingredients_list]

        # check descriptions for gram measurements and brackets
        has_brackets_list = ["(" in i for i in ingredient_amounts_list]
        has_grams_list = [(" g)" in i) or (i[-1] == "g") for i in ingredient_amounts_list]

        # create DataFrame
        self.df = pd.DataFrame(
            {"Recipe": recipes_names_list,
             "Servings": servings_amount_list,
             "Name": ingredient_names_list,
             "Amount": ingredient_amounts_list,
             "Has brackets": has_brackets_list,
             "Has grams": has_grams_list}
        )

        # divide amount description for grams and descriptive measurements
        amount_grams_list = [a.split("(")[1].replace(" g)","") if b else (a.replace(" g", "") if g else 0)
                             for a, b, g in zip(ingredient_amounts_list, has_brackets_list, has_grams_list)]
        amount_description_list = [a if not g else (a.split("(")[0].strip() if b else "")
                                   for a, b, g in zip(ingredient_amounts_list, has_brackets_list, has_grams_list)]

        self.df["Amount (g)"] = [int(a) for a in amount_grams_list]
        self.df["Amount (description)"] = amount_description_list
        self.df["Spice"] = self.df.apply(self.check_if_spice, axis=1)
        self.df = self.df.drop("Has grams", axis=1).drop("Has brackets", axis=1)
        self.grouped_ingredients_df = pd.DataFrame()
        self.group_ingredients_by_name()

    @staticmethod
    def check_if_spice(row):
        if row["Amount (g)"] < 6:
            return True
        return False

    def change_servings_user_input(self):
        """Takes input from user - how many servings for each recipe"""
        target_servings_dict = {}
        for recipe in self.recipe_servings_dict.keys():
            target_servings = input(f"How many servings would you like to prepare of {recipe}?")
            while not target_servings.isdigit() or int(target_servings) < 1:
                target_servings = input(f"Provide a valid (non-negative, non-zero) number (digit) of servings for"
                                        f"{recipe}!")
            target_servings = int(target_servings)
            target_servings_dict[recipe] = target_servings
        self.change_servings(target_servings_dict)

    def change_servings(self, target_servings_dict):
        """Changes ingredients amount in 'Amount (g)' column based on target_servings_dict"""
        multiplication_dict = {}
        for recipe, serving in self.recipe_servings_dict.items():
            multiplication_dict[recipe] = target_servings_dict[recipe]/serving

        # update df, recipe_servings_dict, grouped_ingredients_df
        self.df["Amount (g)"] = self.df.apply(lambda x: self.multiply_ingredients(x, multiplication_dict), axis=1)
        self.recipe_servings_dict = target_servings_dict
        self.group_ingredients_by_name()

    @staticmethod
    def multiply_ingredients(row, multiplication_dict):
        return multiplication_dict[row["Recipe"]] * row["Amount (g)"]

    def group_ingredients_by_name(self):
        self.grouped_ingredients_df = (self.df.groupby("Name", as_index=False)
                                       .agg({"Amount (g)": 'sum', 'Spice': 'min'}))

    def save_groceries_to_xlsx_file(self):
        spices_df = self.grouped_ingredients_df[self.grouped_ingredients_df.Spice == True][["Name", "Amount (g)"]]
        ingredients_df = self.grouped_ingredients_df[self.grouped_ingredients_df.Spice == False][["Name", "Amount (g)"]]

        if not os.path.exists(self.xlsx_file_path):
            pd.DataFrame().to_excel(self.xlsx_file_path, sheet_name='Ingredients')
        with pd.ExcelWriter(self.xlsx_file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            ingredients_df.to_excel(excel_writer=writer, sheet_name='Ingredients', index=False)
            spices_df.to_excel(excel_writer=writer, sheet_name='Spices', index=False)


if __name__ == "__main__":
    groceries = Groceries("../recipes.txt", "../groceries.xlsx")
    # print(groceries.df.to_string())
    # print(groceries.recipe_servings_dict)
    # print(groceries.grouped_ingredients_df)

    groceries.change_servings_user_input()
    # print(groceries.df.to_string())
    # print(groceries.recipe_servings_dict)
    # print(groceries.grouped_ingredients_df)

    groceries.save_groceries_to_xlsx_file()

