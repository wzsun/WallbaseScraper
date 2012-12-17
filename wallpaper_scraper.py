import urllib
import mechanize
import unicodedata

wall_database = []
crypted_database = []
pic_database = []

def getPages():
    # Creates an instance of a browser
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False) #avoids fucken bots -_-

    # Makes you look like a computer
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # Reads wallbase
    wallpaper_page = br.open('http://wallbase.cc/toplist/0/213/eqeq/0x0/0/110/60/1d').read()
    br.close()

    global wall_database
    
    # code
    if(wallpaper_page.find('<div id="thumbs">') > 0):
        while wallpaper_page.find('<div class="thumb') > 0:
            wallpaper_div_start = wallpaper_page.find('<a href="http://wallbase.cc/wallpaper/')
            wallpaper_page = wallpaper_page[wallpaper_div_start+9:]
            wallpaper_end = wallpaper_page.find('" id="')
            wall_database.append(wallpaper_page[:wallpaper_end])
            wallpaper_page[wallpaper_end+1:]
    else:
        print('Shits gone bad, fix it')

def decrypt(encrypted):
    b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    k=0
    l=0
    m=""
    n=[]
    if not encrypted :
        return encrypted
    encrypted += ""
    while True:
        f = b.find(encrypted[k])
        k+=1
        g = b.find(encrypted[k])
        k+=1
        h = b.find(encrypted[k])
        k+=1
        i = b.find(encrypted[k])
        k+=1
        j = f << 18 | g << 12 | h << 6 | i
        c = j >> 16 & 255
        d = j>> 8 & 255
        e = j & 255
        if h == 64:
            n.append(''.join(map(unichr, [c])))
        elif i == 64:
            n.append(''.join(map(unichr, [c,d])))
        else:
            n.append(''.join(map(unichr, [c,d,e])))
        if k >= len(encrypted):
            break
    m = "".join(n)
    return m

def getCryptedLink():
    global wall_database
    global crypted_database
    br = mechanize.Browser()
    
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False) #avoids fucken bots -_-

    # Makes you look like a computer
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    for pic in wall_database:
        pic_page_html = br.open(pic).read()
        pic_page_html = pic_page_html[pic_page_html.find('+B(')+4:]
        pic_page_end = pic_page_html.find("')+'")
        crypted_database.append(pic_page_html[:pic_page_end])
    br.close()

print('Getting Pages')
getPages()

print('Retrieving the crypted links')
getCryptedLink()
print('Done retrieving')

print('Decrypting')
for l in crypted_database:
    pic_database.append(decrypt(l))
print('Done decrypting')
print('Downloading images')


count=0
for img in pic_database:
    print(count)
    urllib.urlretrieve(img,'FileLocation' + str(count)+'.jpg')
    count+=1
    
print('Done')

    
    
    
    
    
