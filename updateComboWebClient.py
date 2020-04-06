import shutil
import distutils.dir_util
import sys
import os
sys.path.insert(0, 'contrib/combo_web_client') 
import buildComboWebClient

def main():
    # get the current running path
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    # build the web client
    build_updated_web_client(dname)

    # copy the results to the correct places
    extract_build_results(dname)
    
    move_assets_if_existing(dname)

    #try:
    #    move_assets_if_existing()
    #except:
    #    print ("No assets found in build")

    setup_html_template(dname)

    print ("Build finished")

def build_updated_web_client(dname):
    # run the sub python script to build from the correct angular folder
    os.chdir(dname + '/contrib/combo_web_client')
    buildComboWebClient.buildComboWebClient()
    os.chdir(dname)

def extract_build_results(dname):
    result_path = dname + '/static/'

    source_path = dname + '/contrib/combo_web_client/dist/'
    files_in_dist = os.listdir(source_path)
    source_path += files_in_dist[0] + "/"

    move_files(source_path, result_path)

def move_assets_if_existing(dname):
    result_path = dname + "/assets/"
    source_path = dname + "/static/assets/"

    move_files(source_path, result_path)

def setup_html_template(dname):
    result_path = dname + "/templates/index.html"
    source_path = dname + "/static/index.html"

    shutil.copy(source_path, result_path)

    # Read in the file
    with open(result_path, 'r') as file :
        filedata = file.read()

    # Replace the sources and hrefs to direct to the static folder
    filedata = filedata.replace('<base href="/">', '<base href="static/">')

    # Write the file out again
    with open(result_path, 'w') as file:
        file.write(filedata)

def move_files(source_path, result_path):
    distutils.dir_util.copy_tree(source_path, result_path)





if (__name__ == '__main__'):
    main()