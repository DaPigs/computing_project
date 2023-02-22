choice = input("Hello! CRUD or WebApp?").lower()
if(choice == "crud"):
    from crud import main
    main()
elif(choice == "webapp"):
    from webapp import app
    app.run(host="0.0.0.0", port=8080)