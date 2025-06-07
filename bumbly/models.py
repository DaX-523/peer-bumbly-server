from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
import uuid
from enum import Enum

# Define enums
class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class ConnectionStatusEnum(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"

# Create your models here.
class User(DjangoCassandraModel):
  id = columns.UUID(primary_key=True, default=uuid.uuid4)
  first_name = columns.Text()
  last_name = columns.Text()
  email = columns.Text()
  password = columns.Text()
  age = columns.Integer()
  gender = columns.Text()  # Will store enum values
  photo_url = columns.Text()
  bio = columns.Text()
  location = columns.Text()
  skills = columns.List(columns.Text())
  interests = columns.List(columns.Text())
  education = columns.List(columns.Text())
  work = columns.List(columns.Text())
  hobbies = columns.List(columns.Text())
  created_at = columns.DateTime()
  updated_at = columns.DateTime()

  def __str__(self): # This special method returns a string version of the model when printed – useful for debugging and the admin panel.
    return self.first_name + " " + self.last_name
  

class ConnectionRequest(DjangoCassandraModel):
  id = columns.UUID(primary_key=True, default=uuid.uuid4)
  from_user_id = columns.UUID()
  to_user_id = columns.UUID()
  status = columns.Text()  # Will store enum values
  created_at = columns.DateTime()
  updated_at = columns.DateTime()

  def __str__(self):
    return f"ConnectionRequest from {self.from_user_id} to {self.to_user_id}"
  

class Chat(DjangoCassandraModel):
   id = columns.UUID(primary_key=True, default=uuid.uuid4)
   sender_id = columns.UUID()
   receiver_id = columns.UUID()
   message = columns.Text()
   created_at = columns.DateTime()
   updated_at = columns.DateTime()

   def __str__(self):
     return f"Chat between {self.sender_id} and {self.receiver_id}"