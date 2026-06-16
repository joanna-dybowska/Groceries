import re
import json
import pymupdf # pip install PyMuPDF

class RecipePDF:
    def __init__(self, pdf_file_path, txt_file_path, pages_numbers_list=None):
        """Get content from PDF file"""
        self.pdf_file_path = pdf_file_path
        self.txt_file_path = txt_file_path

        doc = pymupdf.open(pdf_file_path)
        self.recipe_list = []
        self.title_list = []
        self.servings_list = []

        if pages_numbers_list:
            for page_number in pages_numbers_list:
                page = doc[page_number-1]
                self.extract_recipe_title_servings_from_page(page)
        else:
            for page in doc: # iterate the document pages
                self.extract_recipe_title_servings_from_page(page)
        doc.close()

    def extract_recipe_title_servings_from_page(self, page):
        start = 'Składniki na:'
        end = 'porcj'
        text = page.get_text().strip().replace(" ", "")  # get plain text encoded as UTF-8
        if text:
            recipe = self.get_recipe_ingredients(text)
            if recipe:
                self.recipe_list.append(recipe)
                self.title_list.append(self.get_recipe_title(text))
                self.servings_list.append((text.split(start))[1].split(end)[0].strip())

    @staticmethod
    def get_recipe_ingredients(text):
        text_lines = text.split("\n")
        is_an_ingredient = [True if "•" in line else False for line in text_lines]
        # Finding the line of a recipe without "•" character - on the (i+1) index
        for i in range(0, len(text_lines)-2):
            if is_an_ingredient[i] and not is_an_ingredient[i+1] and is_an_ingredient[i+2]:
                text_lines[i] = text_lines[i].strip()+" "+text_lines[i+1].strip()
        recipe_text_lines = [line.strip().replace("•	 ", "• ").replace("•	", "• ")
                             for line in text_lines if "•" in line]
        recipe = ("\n").join(recipe_text_lines).strip()
        return recipe

    @staticmethod
    def get_recipe_title(text):
        with open("../json/polish_short_words.json", "r", encoding="utf-8-sig") as f:
            polish_short_words = json.load(f)
        upper_case_words = re.findall(r'\b[A-ZĄĆĘŁŃÓŚŹŻ]+\b', text)
        ok_words = [w for w in upper_case_words if (len(w)>2 or w.lower() in polish_short_words)]
        return (" ".join(ok_words)
                .replace("PRZYGOTOWANIE", "")
                .replace("SKŁADNIKI", "")
                .replace("KLIK", "")
                .replace("\n", " ")
                .strip()
                )

    def correct_titles_user_input(self):
        for i, title in enumerate(self.title_list):
            input_title = input(f"Current title: {title}\nIs that proper recipe title? "
                                       f"If yes click ENTER, if not, enter new title: ")
            if input_title:
                self.title_list[i] = input_title

    def save_recipes_txt_file(self):
        file_content = ""
        for t, s, r in zip(self.title_list, self.servings_list, self.recipe_list):
            file_content += f"{t.strip()
            .removesuffix(" C")
            .removesuffix(" W")
            .removesuffix(" Z")} - {s}\n{r.strip()}\n\n"
        file_content = file_content.strip()
        with open(self.txt_file_path, "w", encoding="utf-8-sig") as f:
            f.write(file_content.replace("–", "-"))


if __name__ == "__main__":
    # recipe_pdf = RecipePDF("../Jadłospis-8-dni-DIY.pdf", "../recipes.txt")
    # recipe_pdf.correct_titles_user_input()
    # recipe_pdf.save_recipes_txt_file()

    recipe_pdf = RecipePDF("../results/2000-kcal-DIY-WYSOKOBIALKOWY.pdf", "../test/recipes2.txt",
                           [75, 95, 102, 111, 118, 136, 138, 140])
    recipe_pdf.correct_titles_user_input()
    recipe_pdf.save_recipes_txt_file()
