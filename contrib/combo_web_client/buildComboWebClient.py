import os

def buildComboWebClient():
    try:
        os.mkdir("node_modules") 
    except:
        pass
    
    try:

        if os.system('ng --version') != 0:
            raise Exception('Angular is not installed on this computer')

        if os.system('npm -v') != 0:
            raise Exception('Npm is not installed on this computer')

        os.system('npm install')
        os.system('ng build')
    except:
        print("Something went wrong, couldn't build the angular project")

    print ("Build finished")

if (__name__ == '__main__'):
    buildComboWebClient()