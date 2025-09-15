import uuid
from datetime import datetime
from database import SessionLocal
from models import AdminKey

def generate_key_pair():
    access_key = "admin_" + uuid.uuid4().hex[:8]
    secret_key = uuid.uuid4().hex
    return access_key, secret_key

def insert_admin_key():
    db = SessionLocal()
    access_key, secret_key = generate_key_pair()

    admin = AdminKey(
        access_key=access_key,
        secret_key=secret_key,
        created_at=datetime.utcnow()
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)
    db.close()

    print("✅ Admin key created:")
    print(f"ACCESS_KEY = {access_key}")
    print(f"SECRET_KEY = {secret_key}")

if __name__ == "__main__":
    insert_admin_key()

