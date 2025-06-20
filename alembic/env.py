# alembic/env.py

# Standard imports
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# --- Path Setup ---
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_dir)

# --- Load .env ---
dotenv_path = os.path.join(project_dir, '.env')
print(f"Attempting to load .env file from: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)
DATABASE_URL = os.getenv('DATABASE_URL')

# --- Import Base AND Models ---
target_metadata = None # Initialize to None
try:
    # Import Base first
    from src.core.database import Base
    print("Successfully imported Base from src.core.database")

    # ***** NOW IMPORT YOUR ACTUAL MODEL MODULES *****
    # Adjust paths if your models are not directly under a 'src/models' directory structure
    # Assuming models are in src/models/alert.py and src/models/log.py
    import src.models.alert # This executes alert.py, registering Alert model
    import src.models.incident 
    import src.models.log   # This executes log.py, registering Log model
    # If they were in different locations, import accordingly, e.g.:
    # import app.models.alert
    # import app.models.log
    print("Successfully imported model modules (alert, log)")

    # Assign the metadata *after* all models are imported/registered
    target_metadata = Base.metadata
    print("Assigned Base.metadata to target_metadata")

except ImportError as e:
    print(f"Error importing Base or model modules: {e}")
    print("Please check paths in alembic/env.py and ensure model files exist.")
    # target_metadata remains None if import fails

# --- Alembic Config Setup ---
config = context.config
if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable not found.")
else:
    print(f"DATABASE_URL found: {DATABASE_URL[:15]}...")
    config.set_main_option('sqlalchemy.url', DATABASE_URL)
    print("Alembic config 'sqlalchemy.url' set from environment variable.")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- run_migrations_offline / run_migrations_online Functions ---
# (Make sure target_metadata is passed correctly inside these as before)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata, # Ensure this uses the variable set above
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    if target_metadata is None:
         print("Error: target_metadata is None. Cannot run online migrations for autogenerate.")
         print("Check model imports in env.py.")
         return # Exit early if metadata couldn't be loaded

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata # Ensure this uses the variable set above
        )
        with context.begin_transaction():
            context.run_migrations()

# --- Main Execution Logic ---
if context.is_offline_mode():
    print("Running migrations in offline mode...")
    run_migrations_offline()
else:
    print("Running migrations in online mode...")
    run_migrations_online() # This will now run with populated metadata (if imports succeed)