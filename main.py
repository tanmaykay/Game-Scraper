from steam_scraper import get_all_steam_game_prices
from epic_scraper import get_all_epic_game_prices
from ubisoft_scraper import get_all_ubisoft_game_prices
from flask import Flask, render_template,request

app=Flask(__name__,template_folder='Template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/automation', methods=['POST'])
@app.route('/automation', methods=['POST'])
def run_automation():
    if request.method == 'POST':
        game_name = request.form.get('game_name')
        if game_name:
            prices = complete_automation(game_name)
            return render_template('results.html', game_name=game_name, prices=prices)
        else:
            return "Please enter a game name.", 400  # Bad request if no game name is provided
    return "Invalid request method.", 405

'''def price_checker(game_name, store_name, prices):               #////////////
    print(f"\nPrices for '{game_name}' on {store_name}:\n")
    if isinstance(prices, str):
        print(prices)
    else:
        for idx, price_info in enumerate(prices):
            print(f"Option {idx + 1}:")
            print(f"  Title: {price_info['title']}")
            print(f"  Price: {price_info['saleprice']}")
            print(f"  Original Price: {price_info['originalprice']}")
            print()'''


def complete_automation(game_name):
    # Get prices from Steam
    steam_prices = get_all_steam_game_prices(game_name)

    # Get prices from Ubisoft
    ubisoft_prices = get_all_ubisoft_game_prices(game_name)

    # Return both sets of prices in a dictionary
    return {
        'steam': steam_prices,
        'ubisoft': ubisoft_prices
    }

if __name__ == "__main__":
    '''game_name = 'Far Cry 6'
    complete_automation(game_name)'''
    
    app.run(debug=True)            

    