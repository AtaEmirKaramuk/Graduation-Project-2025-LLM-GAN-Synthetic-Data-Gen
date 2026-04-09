from Utils.field_extractor import extract_form_fields

url = "https://demoqa.com/login"
fields = extract_form_fields(url)
for field in fields:
    print(field)
