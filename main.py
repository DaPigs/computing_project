choice = input("Hello! CRUD or WebApp?").lower()
if(choice == "crud"):
  from crud import main
  main()
elif(choice == "webapp"):
	from webapp import app
	print("\033[93mOpen this link in a new window, if not this project won't work.\nhttps://database-project.zhang-yezhouyez.repl.co/\033[0m")
	import time
	time.sleep(2)
	app.run(host="0.0.0.0", port=8080)