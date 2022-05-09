# dondo
Dondo script

1. Sign up on https://www.digitalocean.com/
2. Create Personal access token: API -> Tokens\Key -> Generate new token and add token to config.ini(section 'do' parameter 'token')
3. Add ssh key: Setting -> Security -> Add SSH Key and add ssh file path/user name/password to config.ini(section 'ssh' parameters 'filePath', 'user_name', 'password')
4. Run python ./setup.py
5. Run python ./main.py