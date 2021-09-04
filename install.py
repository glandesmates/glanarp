import os

if os.path.exists('/usr/bin/gscan'):
  os.system('sudo rm /usr/bin/gscan')
elif os.path.exists('/usr/bin/glap'):
  os.system('sudo rm /usr/bin/glap')

os.system('sudo cp gscan /usr/bin/')
os.system('sudo chmod +x /usr/bin/gscan')
print("You can use gscan in any location with 'gscan' command. You can delete this directory."
