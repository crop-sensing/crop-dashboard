import requests

username = 'audreypet'
token = '0540c9dd2b156af5308aec5ad02d3e97039f98b6'  # found in your PythonAnywhere account

# domain = f"{username}.pythonanywhere.com"

# # 🔄 API endpoint to reload the web app
# url = f"https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/"

# response = requests.get(
#     url,
#     auth=(username, token)
# )

# print(response.text)




file_path = "C:/Users/cpetrosi/Desktop/SAWS_Dashboard/audreypet_pythonanywhere_com_wsgi.py"
upload_path = "/var/www/audreypet_pythonanywhere_com_wsgi.py"

with open(file_path, 'rb') as f:
    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{upload_path}',
        headers={'Authorization': f'Token {token}'},
        files={'content': f}
    )


print(response.status_code)