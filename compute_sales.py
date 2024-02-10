import json
import sys
import time


def load_json_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading {filepath}: {e}")
        return None


def map_prices_to_titles(products):
    prices = {}
    for product in products:
        prices[product['title'].lower()] = product['price']
    return prices


def calculate_total_sales(prices, sales):
    total_cost = 0
    errors = False
    for sale in sales:
        product_name = sale.get('Product').lower()
        quantity = sale.get('Quantity')

        if product_name not in prices:
            print(f"Error: Product '{product_name}' \
                  not found in price catalogue.")
            errors = True
            continue

        try:
            total_cost += prices[product_name] * quantity
        except TypeError:
            print(f"Invalid data for product '{product_name}': \
                  quantity should be a number.")
            errors = True

    return total_cost, errors


def main(price_catalogue_path, sales_record_path):
    start_time = time.time()

    products = load_json_data(price_catalogue_path)
    sales = load_json_data(sales_record_path)

    if products is None or sales is None:
        return

    prices = map_prices_to_titles(products)
    total_cost, errors = calculate_total_sales(prices, sales)

    elapsed_time = time.time() - start_time

    result_str = f"Total Sales Cost: ${total_cost:.2f}\
        \nExecution Time: {elapsed_time:.2f} seconds"
    print(result_str)

    if not errors:
        with open("SalesResults.txt", "a") as file:
            file.write(result_str)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compute_sales.py \
              priceCatalogue.json salesRecord.json")
    else:
        price_catalogue_path = sys.argv[1]
        sales_record_path = sys.argv[2]
        main(price_catalogue_path, sales_record_path)
