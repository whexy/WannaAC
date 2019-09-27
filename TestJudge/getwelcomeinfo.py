def getinfo():
    with open("welcome.info","r") as f:
        return str(f.read())

def setinfo(content):
    with open("welcome.info","w") as f:
        f.write(content)