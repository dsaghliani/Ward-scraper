# The code was taken from:
# https://stackoverflow.com/questions/58103525/how-to-decode-email-xa0protected-while-web-scraping-using-python/58111681#58111681

def decrypt_cloudflare_email(fp):
    r = int(fp[:2],16)
    email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
    return email
