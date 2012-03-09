Android Resources Refactoring Tools

This tools can help you to add a prefix one all your android project resources.

Features:
1). change R.type.your_name to R.type.prefix_your_name
    eg: R.string.app_name to R.string.myprefix_app_name
2). chagne your_name.xml to prefix_your_name.xml
    eg: main_layout.xml to myprefix_main_layout.xml
3). change the name in your xml attribute
    eg: <string name="app_name">My name</string> to <string name="myprefix_app_name">My name</string>
4). change @type/your_name to @type/prefix_your_name
    eg: @drawable/your_image to @drawable/my_prefix_your_image
5). change your asset's file name from your_name.sth to myprefix_your_name.sth
    eg: README.txt to myprefix_README.txt

How to use:
1). put add_prefix.py in your workspace folder, eg: ~/workspace/
2). go to your workspace folder, run add_prefix.py <project_folder_name> <resources_prefix>
