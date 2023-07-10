## Magic the Gathering scripts

Data source: https://mtgjson.com/downloads/all-sets/ (provides json files for all card sets)

- **mtg_json**: Creates a csv file containing set code, name, number, rarity, color identity, and type
for cards and tokens of the given set. 
All cards are sorted in ascending numerical order - depending on preference, special
cards (i.e. etched foil cards in STX) can be filtered out.
- **test_mtg_json**: Unit tests for mtg_json.
- **check_for_special_chars_in_numbers**: Iterates through a given folder containing json files and returns
a csv indicating cards with special characters in their card number for each given set.
- **mtg_tcgp**: Add card counts scanned with the TCG-Player app to the main card database file (created with **mtg_json**).
- **mtg_delver**: Add card counts scanned with the Delver Lens app to the main card database file (created with **mtg_json**).
