import requests

def is_valid_word(word: str, api_key):
    print("Here is the word: " + word)
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'
    response = requests.get(url)
    # print(response.content)
    try:
        data = response.json()
        if response.status_code == 200:
            # Check if the response contains any data
            if data and isinstance(data, list):
                return True
            else:
                return False
        else:
            print("Error accessing the API:", response.status_code)
            return None
    except ValueError as e:
        print("Error decoding JSON:", e)
        return None

if __name__ == "__main__":
    api_key = '57300dd3-e1ec-43cb-81fd-5b44fdf7df7d'


    word = "hi"  # Sample word
    if is_valid_word(word, api_key):
        print(f"'{word}' is a valid word.")
    else:
        print(f"'{word}' is not a valid word.")



