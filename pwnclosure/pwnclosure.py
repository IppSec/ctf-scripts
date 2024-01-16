import fd
import re
import logging
import os

def getLinks(html):
    output = set()
    links = re.findall(r"""(?:href=|src=|include )["']([0-9a-zA-Z\-_\/\.]*)[\?"']""", html)    
    for link in links:
        if not '.' in link:
            link += '/index.php'
        output.add(link)

    # Different regex, because if we just get a item with no extension, its a file.
    # Above, it it probably a directory.
    links = re.findall(r"""page=([0-9a-zA-Z-_\/\.]*)""", html)
    for link in links:
        if not '.' in link:
            link += '.php'
        output.add(link)

    return output


def saveFile(fullPath, content):
    directory = "output" + os.path.dirname(fullPath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open("output" + fullPath, "w") as f:
        f.write(content)    
    
# ToDo: Automatically identify parent based upon webserver config
# func = a call to download src
def startCrawl(func, parent, file):    
    crawled = set()
    queue = {file}
    while queue:
        page = queue.pop()
        crawled.add(page)
        fullPath = parent + page
        output = func(fullPath)
        saveFile(fullPath, output)
        links = getLinks(output)
        for link in links:
            link = link.lstrip("/")
            if link.endswith(".."):
                continue
            if (link not in crawled) and (link not in queue):
                queue.add(link)
                logging.debug(f"Added {link} to queue")       

startCrawl(fd.downloadFile, "/var/www/html/", "index.php")


