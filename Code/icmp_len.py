import pyshark

cap = pyshark.FileCapture(
    'icmp_len.pcap', 
    display_filter="icmp && icmp.type ==8",
    tshark_path=r'E:\CTFTools\Wireshark\tshark.exe')

flag = ''
for packet in cap:
    icmp_len = packet.icmp.data_len
    flag += chr(int(str(icmp_len)))

cap.close()
print(flag)
# ctfhub{acb659f023}