import hashlib

from django.http.request import split_domain_port


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


hash_string = 'confidential data'
sha_signature = encrypt_string(hash_string)
print(sha_signature)


# 3fef7ff0fc1660c6bd319b3a8109fcb9f81985eabcbbf8958869ef03d605a9eb
def split_domain_ports(host):
    domain, port = split_domain_port(host)
    return domain
