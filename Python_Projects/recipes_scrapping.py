from bs4 import BeautifulSoup
import requests

url = "https://www.doradcasmaku.pl/przepisy-obiad-pora-dnia"
base_url = "https://www.doradcasmaku.pl"
titles = []
ingredients = []
all_links = []
for x in range(2):
    print(x)
    if x == 0:
        response = requests.get(url)
    else:
        response = requests.get(url+f",{x}")

    web_content = response.text

    soup = BeautifulSoup(web_content, 'html.parser')

    recipes = soup.find_all(name="h3", class_="recipe_title")
    # print(recipes)
    recipes_urls = []
    for recipe in recipes:
        ingr_url = recipe.find("a")["href"]
        recipes_urls.append(base_url + ingr_url)
        all_links.append(base_url + ingr_url)
    # print(recipes_urls)
    # print(len(recipes_urls))

    for recipe_url in recipes_urls:
        req_ingr = requests.get(recipe_url)
        ingr_soup = BeautifulSoup(req_ingr.text, 'html.parser')
        recipe_title = ingr_soup.find("h1", class_="recipe_name").text
        titles.append(recipe_title)
        ingredients_groups = ingr_soup.find_all("div", class_="ingredients_group")

        ingredients_dict = {}
        for group in ingredients_groups:
            list_ingredient = group.find_all("li")
            # print(list_ingredient)
            for ingr in list_ingredient:
                ingredient_name = ingr.find("p").text
                ingredient_quantity = ingr.find("span").text
                ingredients_dict[ingredient_name] = ingredient_quantity

        ingredients.append(ingredients_dict)



# print(titles)
# print(ingredients)
recipies_dict = {"recipe": []}

for i in range(len(titles)):
    recipies_dict["recipe"].append({"name": titles[i],
                                   "ingredients": ingredients[i],
                                    "link": all_links[i]})

print(recipies_dict)
with open("przepisy.txt", mode="w", encoding='utf8') as file:
    file.write(str(recipies_dict))
