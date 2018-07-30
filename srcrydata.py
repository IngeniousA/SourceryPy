import appsettings
import random
import string
import urllib.request
from pathlib import Path
import os


def initcomps():
    listf = Path(appsettings.cmdlist)
    oplistf = Path(appsettings.opcmdlist)
    logf = Path(appsettings.log)
    opsf = Path(appsettings.ops)
    promosf = Path(appsettings.promos)
    expf = Path(appsettings.expired)
    cachedir = Path(appsettings.cache)
    if not listf.is_file():
        f1 = open(appsettings.cmdlist, "w")
        f1.write(appsettings.listA)
        f1.close()
    if not oplistf.is_file():
        f1 = open(appsettings.opcmdlist, "w")
        f1.write(appsettings.listB)
        f1.close()
    if not logf.is_file():
        f1 = open(appsettings.log, "w")
        f1.write("")
        f1.close()
    if not opsf.is_file():
        f1 = open(appsettings.ops, "w")
        f1.write("493473011")
        f1.close()
    if not promosf.is_file():
        f1 = open(appsettings.promos, "w")
        f1.write("")
        f1.close()
    if not expf.is_file():
        f1 = open(appsettings.expired, "w")
        f1.write("")
        f1.close()
    if not cachedir.is_dir():
        os.makedirs(appsettings.cache)


def getops():
    oplist = list(open(appsettings.ops))
    resoplist = []
    for opword in oplist:
        resoplist.append(opword.replace('\n', ''))
    return resoplist


def getpromos():
    promlist = list(open(appsettings.promos))
    respromlist = []
    for opword in promlist:
        respromlist.append(opword.replace('\n', ''))
    return respromlist


def addexp(promo):
    opfr = open(appsettings.expired, "r")
    prev = opfr.read()
    opfr.close()
    opfw = open(appsettings.expired, "w")
    opfw.write(prev + "\n" + promo)
    opfw.close()


def getexpired():
    promlist = list(open(appsettings.expired))
    respromlist = []
    for opword in promlist:
        respromlist.append(opword.replace('\n', ''))
    return respromlist


def getcmdlist(telid):
    if getops().count(str(telid)):
        return open(appsettings.cmdlist).read() + open(appsettings.opcmdlist).read()
    return open(appsettings.cmdlist).read()


def addop(telid):
    opfr = open(appsettings.ops, "r")
    prev = opfr.read()
    opfr.close()
    opfw = open(appsettings.ops, "w")
    opfw.write(prev + "\n" + telid)
    opfw.close()


def removeop(telid):
    opsl = getops()
    opsl.remove(str(telid))
    opfw = open(appsettings.ops, "w")
    for op in opsl:
        opfw.write(op + "\n")
    opfw.close()


def addpromo(promo):
    opfr = open(appsettings.promos, "r")
    prev = opfr.read()
    opfr.close()
    opfw = open(appsettings.promos, "w")
    opfw.write(prev + "\n" + promo)
    opfw.close()


def promgen(link, size=9, chars=string.ascii_uppercase + string.digits):
    cand = ''.join(random.choice(chars) for _ in range(size))
    full = cand + link
    while getpromos().count(full) > 0 or getexpired().count(cand) > 0:
        cand = ''.join(random.choice(chars) for _ in range(size))
        full = cand + link
    addpromo(full)
    return cand


def isop(telid):
    return getops().count(str(telid)) > 0


def load(link):
    file_name = link.split('/')[-1]
    u = urllib.request.urlopen(link)
    f = open(appsettings.cache + "\\" + file_name, 'wb')

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)

    f.close()
