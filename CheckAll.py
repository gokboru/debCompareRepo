import sys
import re

######
# https://github.com/nyucel/pardus-check/blob/master/get_package_info.py
######
def get_package_info(package_info, info):
    return re.search(info+": (.*)", package_info).group(1)

def get_package_sha256sum(package_info):
    return get_package_info(package_info, 'SHA256')

def get_package_version(package_info):
    return get_package_info(package_info, 'Version')
    
def get_package_name(package_info):
    return get_package_info(package_info, 'Package')

def get_package_filename(package_info):
    return './' + '/'.join(get_package_info(package_info, 'Filename').split('/')[2:])
##Full List
full_list=[]
es_paket=[]
only_deb=[]
only_par=[]
only_vers=[]
###DEBİAN###
debian_file_path = "/home/beyaz/Downloads/ODEV/Debian/Packages"
debian_file = file(debian_file_path).read()
debian_list = debian_file.split('\n\n')
debian_namelist=[]
debian_sha256 = {}
debian_version = {}
print "Debian paket:",len(debian_list)
for debian_info in debian_list:
    if len(debian_info) < 10:
        continue
    #debian_name = get_package_name(debian_info)
    debian_filename = get_package_filename(debian_info)
    debian_namelist.append(debian_filename)
    debian_sha256sum = get_package_sha256sum(debian_info)
    deb_version = get_package_version(debian_info)
    debian_sha256[debian_filename] = debian_sha256sum
    debian_version[debian_filename] = deb_version
###PARDUS####

pardus_file_path = "/home/beyaz/Downloads/ODEV/pardus/Package"
pardus_file = file(pardus_file_path).read()
pardus_list = pardus_file.split('\n\n')
pardus_namelist=[]
pardus_sha256 = {}
pardus_version = {}
print "Pardus paket:",len(pardus_list)
for pardus_info in pardus_list:
    if len(pardus_info) < 10:
        continue
    #pardus_name = get_package_name(pardus_info)
    pardus_filename = get_package_filename(pardus_info)
    pardus_namelist.append(pardus_filename)
    pardus_sha256sum = get_package_sha256sum(pardus_info)
    par_version = get_package_version(pardus_info)
    pardus_sha256[pardus_filename] = pardus_sha256sum
    pardus_version[pardus_filename] = par_version

##test için tam paket sayısı
##for x in pardus_namelist:
##    if x not in full_list:
##        full_list.append(x)
##for y in debian_namelist:
##    if y not in full_list:
##        full_list.append(y)
##print "FullList: "+str(len(full_list))

for paket in pardus_namelist:
    
    try: #pardusdaki paket debianda varsa hata vermez
        if debian_sha256[paket]==pardus_sha256[paket]: #sha'lar aynıysa vers aynı
            es_paket.append(paket.split("/")[3])
        else: #paket var versiyonlar farklı
            debvers=debian_version[paket]
            parvers=pardus_version[paket]
            only_vers.append("  Debian version: "+str(debvers)
                            +"  Pardus version:  "+str(parvers))
        debian_namelist.remove(paket)
    except KeyError: #Hata varsa pardusta olan paket debianda yok
        #OnlyPardus
        only_par.append(paket.split("/")[3])

#Sadece Debian
for deb in debian_namelist:
    only_deb.append(deb.split("/")[3])

print "Toplam: "+str(len(only_deb)+len(only_par)+len(es_paket)+len(only_vers))
