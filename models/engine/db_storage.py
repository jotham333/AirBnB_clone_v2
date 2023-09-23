#!/usr/bin/python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class DBStorage:
    __engine = None
    __session = None
    __class_mapping = {
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def __init__(self):
        """
        Initializes the DBStorage object and establishes a connection to the MySQL database.
        """
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        db = os.getenv('HBNB_MYSQL_DB')
        
        # Create the database URL
        db_url = f"mysql+mysqldb://{user}:{passwd}@localhost:3306/{db}"

        # Create the SQLAlchemy engine
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        # If the environment is set to "test," drop all tables
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Retrieves all instances of a specific class from the database.
        If no class is specified, retrieves all instances from all classes.
        """
        bucket = {}

        if cls:
            if isinstance(cls, str):
                cls = self.__class_mapping.get(cls)

            instances = self.__session.query(cls).all()
            for instance in instances:
                key = f"{instance.__class__.__name__}.{instance.id}"
                bucket[key] = instance

        else:
            for cls_name, cls in self.__class_mapping.items():
                instances = self.__session.query(cls).all()
                for instance in instances:
                    key = f"{cls_name}.{instance.id}"
                    bucket[key] = instance

        return bucket

    def new(self, obj):
        """
        Adds a new instance to the database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits the changes made in the database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an instance from the database session.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates the database tables if they don't exist and creates a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """
        Closes the database session.
        """
        self.__session.close()
