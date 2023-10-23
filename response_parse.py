import re
import uuid


def parse_response(response):
    result_list = []
    # find start of array
    start_index = response.find("[")
    # find end of array
    end_index = response.find("]") + 1
    # array text
    result_text = response[
        start_index + 1 : end_index - 1
    ].strip()  # Just remove outer []

    # Clean up the string by removing newline characters and multiple spaces
    result_text = result_text.replace("\n", "").replace("  ", " ")

    # Use regex to match each result
    pattern = r"\{ name: '(.*?)', lon: '(.*?)', lat: '(.*?)' \}"
    matches = re.findall(pattern, result_text)

    for match in matches:
        unique_id = str(uuid.uuid4())
        result_list.append(
            {
                "clientId": unique_id,
                "location": match[0],
                "longitude": float(match[1]),
                "latitude": float(match[2]),
            }
        )

    return result_list
