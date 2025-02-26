import secrets

# สร้าง JWT_SECRET ที่มีความยาว 32 bytes (256-bit) และเข้ารหัสเป็น hex string
JWT_SECRET = secrets.token_hex(32)
print("JWT_SECRET:", JWT_SECRET)
