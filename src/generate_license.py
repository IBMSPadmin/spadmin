import base64

PASS = "PASS"
def encode(password, cypher, salt = PASS):
    encoded_byte_list = [(ord(a) ^ ord(b)) for a, b in zip(password, cypher)]
    b64_encoded_string = base64.b64encode(bytes(encoded_byte_list)).decode('ascii')
    return salt + b64_encoded_string

def decode (b64_encoded,cypher, salt = PASS):
    if b64_encoded.startswith(salt):
        b64_decoded = list(base64.b64decode(b64_encoded[len(salt):]))
        decoded = [(ord(a) ^ ord(b)) for a, b in zip(''.join([chr(x) for x in b64_decoded]), cypher)]
        decoded_string = ''.join([chr(x) for x in decoded])
        return decoded_string
    else:
        return b64_encoded


cypher = "we_have_worked_in_this_project:a_lot:please_honor_our_work"
valid_to = "01/01/2024" # "%d/%m/%Y"
mac = "2c.7b.08.a0.77.25.11.ee.ab.7b.84.16.0c.a6.5c.e8"

hidedstring = encode(mac+"|"+valid_to, cypher, "SPADMIN")
print("license: ", hidedstring)

print ("check back: ", decode(hidedstring, cypher, "SPADMIN"))
mac_and_validity=decode(hidedstring, cypher,"SPADMIN").split("|", 2)
print ("check back: ", mac_and_validity)