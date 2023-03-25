import requests

def download_data(data_url, output_path):

    response = requests.get(data_url, stream=True, verify=False)

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=4096):
            file.write(chunk)