import requests
from bs4 import BeautifulSoup


def decode_secret_message(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    grid = {}
    max_x = 0
    max_y = 0

    # Find the table containing the coordinates and characters.
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue

        headers = [
            cell.get_text(strip=True).lower()
            for cell in rows[0].find_all(["td", "th"])
        ]

        if not all(
            any(name in header for header in headers)
            for name in ["x-coordinate", "character", "y-coordinate"]
        ):
            continue

        x_col = next(i for i, h in enumerate(headers) if "x-coordinate" in h)
        char_col = next(i for i, h in enumerate(headers) if "character" in h)
        y_col = next(i for i, h in enumerate(headers) if "y-coordinate" in h)

        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if len(cells) <= max(x_col, char_col, y_col):
                continue

            x = int(cells[x_col].get_text(strip=True))
            char = cells[char_col].get_text(strip=True)
            y = int(cells[y_col].get_text(strip=True))

            grid[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        break
    else:
        raise ValueError("Could not find the coordinate table in the document.")

    # Print from highest y to lowest y so the graphic is correctly oriented.
    for y in range(max_y, -1, -1):
        line = "".join(
            grid.get((x, y), " ")
            for x in range(max_x + 1)
        )
        print(line)


# Example
decode_secret_message(
    "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
)