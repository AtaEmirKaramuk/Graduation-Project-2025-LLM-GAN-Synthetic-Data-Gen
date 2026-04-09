from PythonScripts.TestDataProject.web_input_module.url_data_handler import process_url_to_data
from PythonScripts.settings import URL


def run_url_pipeline():
    print(f"Running contextual data generation for: {URL}")
    process_url_to_data(URL)

if __name__ == "__main__":
    run_url_pipeline()
