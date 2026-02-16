"""
Generate .streamlit/secrets.toml from environment variables for Render deployment.
This runs before Streamlit starts.
"""
import os

secrets_dir = ".streamlit"
secrets_file = os.path.join(secrets_dir, "secrets.toml")

# Only create if it doesn't already exist
if not os.path.exists(secrets_file):
    os.makedirs(secrets_dir, exist_ok=True)
    
    content = f"""[supabase]
host = "{os.environ.get('SUPABASE_HOST', '')}"
port = {os.environ.get('SUPABASE_PORT', '5432')}
database = "{os.environ.get('SUPABASE_DATABASE', 'postgres')}"
user = "{os.environ.get('SUPABASE_USER', '')}"
password = "{os.environ.get('SUPABASE_PASSWORD', '')}"

[openai]
api_key = "{os.environ.get('OPENAI_API_KEY', '')}"

[admin]
password = "{os.environ.get('ADMIN_PASSWORD', 'admin123')}"
"""
    
    with open(secrets_file, "w") as f:
        f.write(content)
    
    print(f"Created {secrets_file}")
else:
    print(f"{secrets_file} already exists, skipping.")
