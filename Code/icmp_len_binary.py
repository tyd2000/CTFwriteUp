import pyshark

cap = pyshark.FileCapture(
    'icmp_len_binary.pcap', 
    display_filter="icmp && icmp.type ==8",
    tshark_path=r'E:\CTFTools\Wireshark\tshark.exe')

s = ''
for packet in cap:
    icmp_len = int(str(packet.icmp.data_len))
    if icmp_len == 32:
        s += '0'
    else:   # icmp == 64
        s += '1'
# print(s)
def bin_to_ascii(bin_str):
    ascii_str = ''
    for i in range(0, len(bin_str), 8):
        byte = int(bin_str[i:i+8], 2)
        ascii_str += chr(byte)
    return ascii_str

flag = bin_to_ascii(s)
cap.close()
print(flag)
# ctfhub{04efed1e05}