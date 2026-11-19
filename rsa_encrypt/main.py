from generator import RSAKeyGenerator


def main():
    g = RSAKeyGenerator(61, 53)
    pub = g.public_key()
    prv = g.private_key()
    print("public: ", pub)
    print("private:", prv)

    m = 65
    c = g.encrypt(m)
    d = g.decrypt(c)
    print(f"m={m}, c={c}, d={d}, ok={m == d}")

    message = "hello, world!"
    encrypted = g.encrypt_message(message)
    decrypted = g.decrypt_message(encrypted)
    print(
        f"message={message}, encrypted={encrypted}, decrypted={decrypted}, ok={message == decrypted}"
    )


if __name__ == "__main__":
    main()
