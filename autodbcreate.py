import subprocess

DB_USER = "thony123"
DB_PASS = "mypassword"
DB_NAME = "mydatabase"

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Xato:", result.stderr.strip())
    else:
        print("✅", " ".join(cmd))
    return result

run_cmd([
    "psql", "-d", "postgres", "-c",
    f"DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='{DB_USER}') "
    f"THEN CREATE ROLE {DB_USER} LOGIN PASSWORD '{DB_PASS}' CREATEDB; END IF; END $$;"
])

check_db = run_cmd([
    "psql", "-d", "postgres", "-tAc",
    f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';"
])

if check_db.stdout.strip() != "1":
    run_cmd([
        "psql", "-d", "postgres", "-c",
        f"CREATE DATABASE {DB_NAME} OWNER {DB_USER};"
    ])
else:
    print(f"✅ Database '{DB_NAME}' allaqachon mavjud")
