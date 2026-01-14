#!/usr/bin/env python3
"""
Script to populate Monty's Legacy menu content from data.
Creates category directories and markdown files for each menu item.
"""

import os
import re
from datetime import datetime
from pathlib import Path

# Menu data from image
MENU_DATA = [
    # Beer
    {"name": "420 Orig", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Carib", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Coors Light", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Corona", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Heineken", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Magnum", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Modello", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Rude Boy Stout", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Smirnoff Apple", "category": "Beer", "department": "Bar", "price": 15.00},
    {"name": "Stag", "category": "Beer", "department": "Bar", "price": 15.00},
    
    # Brandy
    {"name": "Hennessy 1/2", "category": "Brandy", "department": "Bar", "price": 150.00},
    {"name": "Hennessy Btl", "category": "Brandy", "department": "Bar", "price": 750.00},
    {"name": "Hennessy Drink", "category": "Brandy", "department": "Bar", "price": 60.00},
    
    # Cocktails
    {"name": "Pain Killer", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Mermaid Rum Punch", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Puncheon Fizz", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Amaretto Sour", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Daiquiri", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Long Island Iced Tea", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Margarita", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Martini", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Midnights at Monty's", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Mudslide", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Pina Colada", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Rick and Monty's", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Sex on the Beach", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Tequila Sunrises", "category": "Cocktails", "department": "Bar", "price": 65.00},
    {"name": "Tropical Monty's", "category": "Cocktails", "department": "Bar", "price": 65.00},
    
    # Food
    {"name": "Chicken Tenders", "category": "Food", "department": "Kitchen", "price": 60.00},
    {"name": "Fried Pork", "category": "Food", "department": "Kitchen", "price": 65.00},
    {"name": "Geera Pork", "category": "Food", "department": "Kitchen", "price": 65.00},
    {"name": "Fried Wontons", "category": "Food", "department": "Kitchen", "price": 55.00},
    {"name": "Hong Kong Wontons", "category": "Food", "department": "Kitchen", "price": 55.00},
    {"name": "Fries", "category": "Food", "department": "Kitchen", "price": 25.00},
    {"name": "Pepper Fries", "category": "Food", "department": "Kitchen", "price": 30.00},
    {"name": "Loaded Fries", "category": "Food", "department": "Kitchen", "price": 45.00},
    {"name": "Pork & Fries", "category": "Food", "department": "Kitchen", "price": 65.00},
    {"name": "Fried Wings", "category": "Food", "department": "Kitchen", "price": 65.00},
    {"name": "Honey Mustard Wings", "category": "Food", "department": "Kitchen", "price": 70.00},
    {"name": "BBQ Wings", "category": "Food", "department": "Kitchen", "price": 70.00},
    {"name": "Fried Wings & Fries", "category": "Food", "department": "Kitchen", "price": 80.00},
    
    # Gin
    {"name": "Bombay Sapphire Gin Drink", "category": "Gin", "department": "Bar", "price": 50.00},
    {"name": "Gordon's Dry", "category": "Gin", "department": "Bar", "price": 45.00},
    {"name": "Jagermeister Drink", "category": "Gin", "department": "Bar", "price": 50.00},
    {"name": "Tanqueray Btl", "category": "Gin", "department": "Bar", "price": 450.00},
    {"name": "Vanguard Gin Drink", "category": "Gin", "department": "Bar", "price": 50.00},
    
    # Pool
    {"name": "Pool per Hour", "category": "Pool", "department": "Games", "price": 40.00},
    
    # Rum
    {"name": "Angostura 7yr Drink", "category": "Rum", "department": "Bar", "price": 50.00},
    {"name": "Angostura Single Barrel Drink", "category": "Rum", "department": "Bar", "price": 60.00},
    {"name": "Bacardi 8yr Drink", "category": "Rum", "department": "Bar", "price": 50.00},
    {"name": "Baileys Btl", "category": "Rum", "department": "Bar", "price": 350.00},
    {"name": "Barcardi Btl", "category": "Rum", "department": "Bar", "price": 500.00},
    {"name": "Black Label Btl", "category": "Rum", "department": "Bar", "price": 750.00},
    {"name": "Campari", "category": "Rum", "department": "Bar", "price": 45.00},
    {"name": "Malibu Btl", "category": "Rum", "department": "Bar", "price": 350.00},
    {"name": "Puncheon", "category": "Rum", "department": "Bar", "price": 45.00},
    {"name": "Royal Oak Btl", "category": "Rum", "department": "Bar", "price": 500.00},
    {"name": "Single Barrel", "category": "Rum", "department": "Bar", "price": 60.00},
    {"name": "Tamboo Btl", "category": "Rum", "department": "Bar", "price": 500.00},
    {"name": "Village Puncheon Drink", "category": "Rum", "department": "Bar", "price": 45.00},
    {"name": "White Oak", "category": "Rum", "department": "Bar", "price": 50.00},
    
    # Scotch
    {"name": "Black & White Btl", "category": "Scotch", "department": "Bar", "price": 400.00},
    {"name": "Dewars 12 Btl", "category": "Scotch", "department": "Bar", "price": 500.00},
    {"name": "Fireball Btl", "category": "Scotch", "department": "Bar", "price": 350.00},
    {"name": "Jack Daniels Apple Btl", "category": "Scotch", "department": "Bar", "price": 500.00},
    {"name": "Jack Daniels Btl", "category": "Scotch", "department": "Bar", "price": 600.00},
    {"name": "Jack Daniels Honey Btl", "category": "Scotch", "department": "Bar", "price": 500.00},
    {"name": "JWB Btl", "category": "Scotch", "department": "Bar", "price": 750.00},
    {"name": "JWB Double Blk", "category": "Scotch", "department": "Bar", "price": 750.00},
    {"name": "Old Par Btl", "category": "Scotch", "department": "Bar", "price": 450.00},
    
    # Shots
    {"name": "Baby Guiness", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Blowjob", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Bob Marley", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Brain Hemorrhage", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Helium Shot", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Jaggerbomb shot", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Lick my Banana", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Liquid Cocaine", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Sex in the Pool", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "Tequila Shots", "category": "Shots", "department": "Bar", "price": 50.00},
    {"name": "The Dirty Monty's", "category": "Shots", "department": "Bar", "price": 50.00},
    
    # Soft
    {"name": "Coke", "category": "Soft", "department": "Bar", "price": 8.00},
    {"name": "CranWater", "category": "Soft", "department": "Bar", "price": 8.00},
    {"name": "Gatorade", "category": "Soft", "department": "Bar", "price": 12.00},
    {"name": "Ginger Ale", "category": "Soft", "department": "Bar", "price": 8.00},
    {"name": "Ginseng Up", "category": "Soft", "department": "Bar", "price": 10.00},
    {"name": "LLB", "category": "Soft", "department": "Bar", "price": 10.00},
    {"name": "Malta", "category": "Soft", "department": "Bar", "price": 10.00},
    {"name": "Monster", "category": "Soft", "department": "Bar", "price": 15.00},
    {"name": "Orchard 1L", "category": "Soft", "department": "Bar", "price": 12.00},
    {"name": "Red Bull", "category": "Soft", "department": "Bar", "price": 15.00},
    {"name": "Shandy", "category": "Soft", "department": "Bar", "price": 12.00},
    {"name": "Soda", "category": "Soft", "department": "Bar", "price": 8.00},
    {"name": "Sprite", "category": "Soft", "department": "Bar", "price": 8.00},
    {"name": "Tonic Water", "category": "Soft", "department": "Bar", "price": 8.00},
    {"name": "Water-500ml", "category": "Soft", "department": "Bar", "price": 8.00},
    {"name": "Water-300ml", "category": "Soft", "department": "Bar", "price": 5.00},
    
    # Tequila
    {"name": "Margaritaville Silver", "category": "Tequila", "department": "Bar", "price": 50.00},
    {"name": "Cafe Patron Btl", "category": "Tequila", "department": "Bar", "price": 650.00},
    {"name": "Jose Cuervo Gold Btl", "category": "Tequila", "department": "Bar", "price": 500.00},
    {"name": "Jose Cuervo Tube", "category": "Tequila", "department": "Bar", "price": 150.00},
    {"name": "Patron Silver Btl", "category": "Tequila", "department": "Bar", "price": 750.00},
    {"name": "Tequila Rose Btl", "category": "Tequila", "department": "Bar", "price": 350.00},
    
    # Vodka
    {"name": "Ketel One Vodka Drink", "category": "Vodka", "department": "Bar", "price": 50.00},
    {"name": "Absolut Btl", "category": "Vodka", "department": "Bar", "price": 450.00},
    {"name": "Absolut Vodka 1/2", "category": "Vodka", "department": "Bar", "price": 250.00},
    {"name": "Grey Goose Btl", "category": "Vodka", "department": "Bar", "price": 600.00},
    {"name": "Tito's Btl", "category": "Vodka", "department": "Bar", "price": 500.00},
    
    # Wine
    {"name": "Barefoot Moscato Btl", "category": "Wine", "department": "Bar", "price": 200.00},
    {"name": "Barefoot Rose Btl", "category": "Wine", "department": "Bar", "price": 200.00},
]


def generate_filename(title):
    """Generate URL-safe filename from title."""
    filename = title.lower()
    # Replace spaces and special characters with hyphens
    filename = re.sub(r'[^a-z0-9]+', '-', filename)
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    return filename


def parse_price_size_flavour(name):
    """Parse size and flavour from item name."""
    size = "-"
    flavour = "-"
    
    name_lower = name.lower()
    
    # Check for size indicators
    if "btl" in name_lower or "bottle" in name_lower:
        size = "Bottle"
    elif "1/2" in name_lower or "half" in name_lower:
        size = "1/2 Bottle"
    elif "drink" in name_lower:
        size = "Drink"
    elif "shot" in name_lower:
        size = "Shot"
    elif "nip" in name_lower:
        size = "Nip"
    elif "tube" in name_lower:
        size = "Tube"
    
    # Extract clean title (remove size indicators for display)
    clean_title = name
    clean_title = re.sub(r'\s+(Btl|Bottle|Drink|Shot|Nip|Tube|1/2)$', '', clean_title, flags=re.IGNORECASE)
    clean_title = re.sub(r'\s+1/2\s+', ' ', clean_title)
    
    return clean_title, size, flavour


def get_ingredients_cookingmethods_types(name, title, category):
    """Determine ingredients, cookingmethods, and types based on item name and category."""
    name_lower = name.lower()
    title_lower = title.lower()
    ingredients = []
    cookingmethods = []
    types = []
    tags = [title]
    
    # Food category
    if category == "Food":
        types.append("Food")
        
        # Chicken items
        if "chicken" in name_lower or "wings" in name_lower or "tenders" in name_lower:
            ingredients.append("Chicken")
            tags.append("Chicken")
            if "wings" in name_lower:
                ingredients.append("BBQ Sauce" if "bbq" in name_lower else "Sauce")
                ingredients.append("Spices")
                tags.append("Wings")
                if "bbq" in name_lower:
                    cookingmethods.append("Fried")
                elif "honey mustard" in name_lower:
                    ingredients.append("Honey Mustard")
                    cookingmethods.append("Fried")
                else:
                    cookingmethods.append("Fried")
            elif "tenders" in name_lower:
                cookingmethods.append("Fried")
                types.append("Appetizer")
        
        # Pork items
        elif "pork" in name_lower:
            ingredients.append("Pork")
            tags.append("Pork")
            if "fried" in name_lower:
                cookingmethods.append("Fried")
            elif "geera" in name_lower:
                ingredients.append("Geera Seasoning")
                cookingmethods.append("Fried")
            if "fries" in name_lower:
                ingredients.append("Potatoes")
                types.append("Combo")
            else:
                types.append("Appetizer")
        
        # Wontons
        elif "wonton" in name_lower:
            ingredients.append("Wonton Wrappers")
            ingredients.append("Filling")
            cookingmethods.append("Fried")
            types.append("Appetizer")
        
        # Fries
        elif "fries" in name_lower:
            ingredients.append("Potatoes")
            cookingmethods.append("Fried")
            types.append("Side")
            if "loaded" in name_lower:
                ingredients.append("Cheese")
                ingredients.append("Toppings")
            elif "pepper" in name_lower:
                ingredients.append("Pepper Seasoning")
        
        # Wings & Fries combo
        if "wings" in name_lower and "fries" in name_lower:
            ingredients.append("Potatoes")
            types.append("Combo")
    
    # Cocktails
    elif category == "Cocktails":
        types.append("Cocktail")
        if "margarita" in name_lower:
            ingredients.extend(["Tequila", "Triple Sec", "Lime Juice"])
        elif "daiquiri" in name_lower:
            ingredients.extend(["Rum", "Lime Juice", "Simple Syrup"])
        elif "martini" in name_lower:
            ingredients.extend(["Gin", "Vermouth"])
        elif "pina colada" in name_lower:
            ingredients.extend(["Rum", "Coconut Cream", "Pineapple Juice"])
        elif "mudslide" in name_lower:
            ingredients.extend(["Vodka", "Kahlua", "Baileys", "Cream"])
        elif "sex on the beach" in name_lower:
            ingredients.extend(["Vodka", "Peach Schnapps", "Cranberry Juice", "Orange Juice"])
        elif "pain killer" in name_lower:
            ingredients.extend(["Rum", "Coconut Cream", "Pineapple Juice", "Orange Juice"])
        elif "mermaid rum punch" in name_lower or "puncheon fizz" in name_lower:
            ingredients.extend(["Rum", "Juice", "Syrup"])
        elif "amaretto sour" in name_lower:
            ingredients.extend(["Amaretto", "Lemon Juice", "Simple Syrup"])
        elif "long island iced tea" in name_lower:
            ingredients.extend(["Vodka", "Tequila", "Rum", "Gin", "Triple Sec", "Lemon Juice", "Cola"])
        elif "tequila sunrise" in name_lower:
            ingredients.extend(["Tequila", "Orange Juice", "Grenadine"])
        elif "monty" in name_lower:
            ingredients.extend(["Rum", "Juices", "Syrups"])
    
    # Shots
    elif category == "Shots":
        types.append("Shot")
        if "baby guinness" in name_lower:
            ingredients.extend(["Coffee Liqueur", "Irish Cream"])
        elif "brain hemorrhage" in name_lower:
            ingredients.extend(["Peach Schnapps", "Irish Cream", "Grenadine"])
        elif "liquid cocaine" in name_lower:
            ingredients.extend(["Jägermeister", "Rumple Minze", "Goldschlager"])
        elif "jaggerbomb" in name_lower:
            ingredients.extend(["Jägermeister", "Red Bull"])
        elif "tequila" in name_lower:
            ingredients.append("Tequila")
        elif "sex in the pool" in name_lower:
            ingredients.extend(["Vodka", "Blue Curacao", "Pineapple Juice"])
    
    # Beer
    elif category == "Beer":
        types.append("Beer")
        ingredients.append("Barley")
    
    # Wine
    elif category == "Wine":
        types.append("Wine")
        if "moscato" in name_lower:
            ingredients.append("Moscato Grapes")
        elif "rose" in name_lower:
            ingredients.append("Red Grapes")
    
    # Spirits categories (Brandy, Gin, Rum, Scotch, Tequila, Vodka)
    elif category in ["Brandy", "Gin", "Rum", "Scotch", "Tequila", "Vodka"]:
        types.append(category)
        if "hennessy" in name_lower:
            ingredients.append("Cognac")
        elif "tanqueray" in name_lower or "gordon" in name_lower or "bombay" in name_lower:
            ingredients.append("Gin")
        elif "bacardi" in name_lower or "puncheon" in name_lower or "angostura" in name_lower:
            ingredients.append("Rum")
        elif "jack daniels" in name_lower or "jwb" in name_lower or "dewars" in name_lower:
            ingredients.append("Whiskey")
        elif "patron" in name_lower or "jose cuervo" in name_lower:
            ingredients.append("Tequila")
        elif "grey goose" in name_lower or "absolut" in name_lower or "ketel one" in name_lower or "tito" in name_lower:
            ingredients.append("Vodka")
    
    # Soft drinks
    elif category == "Soft":
        types.append("Non-Alcoholic")
        if "water" in name_lower:
            ingredients.append("Water")
        elif "coke" in name_lower or "soda" in name_lower:
            ingredients.append("Carbonated Water")
            ingredients.append("Sugar")
        elif "sprite" in name_lower:
            ingredients.append("Carbonated Water")
            ingredients.append("Lemon-Lime Flavor")
        elif "red bull" in name_lower or "monster" in name_lower:
            ingredients.append("Energy Drink")
        elif "gatorade" in name_lower:
            ingredients.append("Sports Drink")
        elif "ginger ale" in name_lower:
            ingredients.append("Ginger")
            ingredients.append("Carbonated Water")
        elif "tonic water" in name_lower:
            ingredients.append("Tonic Water")
            ingredients.append("Quinine")
    
    # Pool
    elif category == "Pool":
        types.append("Game")
    
    # Format arrays as YAML strings
    def format_yaml_array(arr):
        if not arr:
            return "[]"
        return "[" + ", ".join([f'"{item}"' for item in arr]) + "]"
    
    return format_yaml_array(tags), format_yaml_array(ingredients), format_yaml_array(cookingmethods), format_yaml_array(types)


def generate_markdown(item_data):
    """Generate markdown content for a menu item."""
    name = item_data["name"]
    category = item_data["category"]
    price = item_data["price"]
    
    # Parse size/flavour from name
    title, size, flavour = parse_price_size_flavour(name)
    
    # Get ingredients, cookingmethods, types
    tags_str, ingredients_str, cookingmethods_str, types_str = get_ingredients_cookingmethods_types(name, title, category)
    
    # Generate frontmatter
    frontmatter = f"""---
title: {title}
weight: 10
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}Z
prices:
  - size: "{size}"
    price: {int(price) if price == int(price) else price}
    flavour: "{flavour}"
tags: {tags_str}
ingredients: {ingredients_str}
cookingmethods: {cookingmethods_str}
types: {types_str}
events: []
---

"""
    
    return frontmatter


def generate_category_index(category_name):
    """Generate _index.md for a category."""
    content = f"""---
title: {category_name}
weight: 10
---
"""
    return content


def main():
    """Main function to populate menu content."""
    # Get script directory and content directory
    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / "content"
    
    # Ensure content directory exists
    content_dir.mkdir(parents=True, exist_ok=True)
    
    # Group items by category
    categories = {}
    for item in MENU_DATA:
        category = item["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    # Create category directories and files
    for category, items in categories.items():
        category_dir = content_dir / category.lower()
        category_dir.mkdir(exist_ok=True)
        
        # Create _index.md for category
        index_file = category_dir / "_index.md"
        if not index_file.exists():
            index_content = generate_category_index(category)
            index_file.write_text(index_content)
            print(f"Created category index: {index_file}")
        
        # Create markdown files for each item
        for item in items:
            filename = generate_filename(item["name"])
            file_path = category_dir / f"{filename}.md"
            
            markdown = generate_markdown(item)
            file_path.write_text(markdown)
            if file_path.exists():
                print(f"Updated menu item: {file_path}")
            else:
                print(f"Created menu item: {file_path}")
    
    print(f"\nSuccessfully populated {len(MENU_DATA)} menu items across {len(categories)} categories!")


if __name__ == "__main__":
    main()
