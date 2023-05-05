#!/bin/python3
import http.client
import base64
import json

with open("/home/shyju/dsign/sample.pdf", "rb") as pdf_file_to_sign:
    encoded_pdf_bas64_bytes = base64.b64encode(pdf_file_to_sign.read())


conn = http.client.HTTPSConnection("prime-dsa-devctr.docusign.net:8081")

payload = \
"{ \"CreateAndSignField\" : " + \
    "{   \"file\": " + "\"" + encoded_pdf_bas64_bytes.decode("utf-8") + "\", " + \
        "\"fileType\": \"PDF\", " + \
        "\"x\": \"91\", " + \
        "\"width\": \"0\", " + \
        "\"y\": \"164\", " + \
        "\"height\": \"0\", " + \
        "\"page\": \"1\", " + \
        "\"timeFormat\": \"h:mm:ss\", " + \
        "\"dateFormat\": \"dd/MM/yyyy\", " + \
        "\"appearance\": [\"GRAPHICAL_IMAGE\", \"SIGNED_BY\", \"TIME\"]" + \
    "}" + \
"}"

#dsa_basic_auth_bytes = base64.b64encode(bytes("{dsa-user-name}"+":"+"{dsa-user-password}","utf-8"))
dsa_basic_auth_bytes = base64.b64encode(bytes("shyju@epillars.com"+":"+"epillars12","utf-8"))
dsa_basic_auth_string = dsa_basic_auth_bytes.decode("utf-8") 
print (dsa_basic_auth_bytes,"dsa_basic_auth_bytes")
headers = {
    'authorization': "Basic " + dsa_basic_auth_string,
    'content-type': "application/json"
    }

conn.request("PUT", "/sapiws/v1/digital_signature", payload, headers)

res = conn.getresponse()
data = res.read()
rspObj = json.loads(data.decode("utf-8"))

binary_signed_file_string = base64.b64decode(rspObj['signedFile'])
print (rspObj,"@"*80)
with open("/home/shyju/dsign/sample_signed.pdf", "wb") as signed_pdf_file:
    signed_pdf_file.write(binary_signed_file_string);

print("Signed File saved" )

