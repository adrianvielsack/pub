import os, time, balloon
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

USER=""
PASSWD=""
WORDPRESS_URL=""
URL="https://" + WORDPRESS_URL + "/xmlrpc.php"
MESHLAB_SERVER = ""
MESHLAB_SCRIPT = ""
NEW_SUFFIX="-conv"
client = Client(URL, USER, PASSWD)
FOLDER = ""
print "Monitoring:", FOLDER

balloon.balloon_tip("Watching...", FOLDER)

def search_recursive(folder):
    dirs = os.listdir(folder)
    for dirr in dirs:
        if not os.path.isdir(os.path.join(FOLDER, dirr)):
            search_recursive(os.path.join(FOLDER, dirr))
            continue
        files = os.listdir(os.path.join(FOLDER, dirr))
        
        files = [n for n in files if os.path.isfile(os.path.join(FOLDER, dirr, n))]
        if (len([n for n in files if n.find(NEW_SUFFIX + ".stl") >0]) == 0):
                print "Needs Conversion", files
                time.sleep(2)
                plys = [os.path.join(FOLDER, dirr,n) for n in files if n.endswith(".ply")]
                print plys
                for f in plys:
                    stl = f.rstrip(".ply") + NEW_SUFFIX + ".stl"
                    balloon.balloon_tip("Converting ...", f.split("\\")[-1])
                    os.system(MESHLAB_SERVER + " -i " + f + " -o " + stl + " -s " + MESHLAB_SCRIPT)
                    data = {
                        'name': stl.split("\\")[-1]
                        }
                    with open(stl, "rb") as img:
                        data['bits'] = xmlrpc_client.Binary(img.read())
                    balloon.balloon_tip("Uploading ...", f.split("\\")[-1])
                    print client.call(media.UploadFile(data))
                    balloon.balloon_tip("Done", f.split("\\")[-1])
                    continue;
while 1:
    search_recursive(FOLDER)
    time.sleep(1)
