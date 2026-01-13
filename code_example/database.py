from sqlmodel import Session, SQLModel, create_engine

# SQLite database file name
sqlite_file_name = "database.db"
# Database connection URL. For SQLite, it starts with sqlite:///
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False is needed only for SQLite. It allows more than one thread
# to interact with the database for the same connection.
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """
    Creates the database tables based on the SQLModel metadata.
    This checks all classes inheriting from SQLModel with table=True.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency function to provide a database session.
    This yields a session to be used in a request and ensures it is closed afterwards.
    """
    with Session(engine) as session:
        yield session
