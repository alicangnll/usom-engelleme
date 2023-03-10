import requests, shutil, pyfiglet, sys, os, ctypes, win32com.shell.shell, win32event, win32process, random


if sys.platform.startswith("linux") or sys.platform == "darwin":
    hosts_path = r"/etc/hosts"
else:
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
getir_usom = "https://www.usom.gov.tr/url-list.txt"
yonlendir = "127.0.0.1"
ascii_banner = pyfiglet.figlet_format("USOM URL Filter")

print("================================")
print(ascii_banner)
print("07.02.2023 - Güneydoğu Anadolu depremi asla unutulmayacak!")
print("================================")

def elevate():
    outpath = r'%s\%s.out' % (os.environ["TEMP"], os.path.basename(__file__))
    if ctypes.windll.shell32.IsUserAnAdmin():
        if os.path.isfile(outpath):
            sys.stderr = sys.stdout = open(outpath, 'w', 0)
        return
    with open(outpath, 'w+', 0) as outfile:
        hProc = win32com.shell.shell.ShellExecuteEx(lpFile=sys.executable, \
            lpVerb='runas', lpParameters=' '.join(sys.argv), fMask=64, nShow=0)['hProcess']
        while True:
            hr = win32event.WaitForSingleObject(hProc, 40)
            while True:
                line = outfile.readline()
                if not line: break
                sys.stdout.write(line)
            if hr != 0x102: break
    os.remove(outpath)
    sys.stderr = ''
    sys.exit(win32process.GetExitCodeProcess(hProc))

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
        return local_filename

def main():
    download_file(getir_usom)
    try:
        fname = str("hosts_backup_" + str(random.randint(1000,9999999)))
        print("Hosts dosyası yedekleniyor... (" + fname + ")")
        print("================================")
        shutil.copy(hosts_path, fname) # Backup file
        os.remove(hosts_path)
        f = open(hosts_path, "a")
        f.write("# Hosts file!\n")
        f.close()
        for i in open("url-list.txt", "r+"):
            with open(hosts_path, "a") as hostfile:
                gelendata = yonlendir + " " + i.replace(" ", "")
                print(i.replace(" ", "") + " engellendi!")
                hostfile.write(gelendata)
            hostfile.close()
    except(PermissionError):
        print("Maalesef gerekli yetki yok gibi görünüyor. \nDosya değiştirilmiş olabilir " + hosts_path + " dosyasını kontrol edin.")

if __name__ == '__main__':
    main()
