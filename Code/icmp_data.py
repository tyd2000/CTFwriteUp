import pyshark

cap = pyshark.FileCapture(
    'icmp_data.pcap', 
    display_filter="icmp && icmp.type==8",
    tshark_path=r'E:\CTFTools\Wireshark\tshark.exe')

flag = ''
for packet in cap:
    try:
        data_hex = packet.icmp.data[16:18]
        flag += chr(int(data_hex,16))
        # flag += bytes.fromhex(data_hex).decode('utf-8')
    except:
        continue
cap.close()
print(flag)
# ctfhub{c87eb997966acb}