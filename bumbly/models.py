from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
from enum import Enum
import time
import random

# Define enums
class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class ConnectionStatusEnum(Enum):
    IGNORED = "ignored"
    INTERESTED = "interested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

def generate_id():
    """Generate a unique integer ID based on timestamp and random number"""
    timestamp = int(time.time() * 1000)  # milliseconds
    random_part = random.randint(100, 999)
    return int(f"{timestamp}{random_part}")

# Create your models here.
class User(DjangoCassandraModel):
  id = columns.BigInt(primary_key=True)
  first_name = columns.Text()
  last_name = columns.Text()
  email = columns.Text()
  password = columns.Text()
  age = columns.Integer()
  gender = columns.Text()  
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

  def save(self):
    if not self.id:
      self.id = generate_id()
    super().save()

  def __str__(self): # This special method returns a string version of the model when printed – useful for debugging and the admin panel.
    return self.first_name + " " + self.last_name
  

class ConnectionRequest(DjangoCassandraModel):
  id = columns.BigInt(primary_key=True)
  from_user_id = columns.BigInt()
  to_user_id = columns.BigInt()
  status = columns.Text()  # Will store enum values
  created_at = columns.DateTime()
  updated_at = columns.DateTime()

  def save(self):
    if not self.id:
      self.id = generate_id()
    super().save()

  def __str__(self):
    return f"ConnectionRequest from {self.from_user_id} to {self.to_user_id}"
  
class SuperConnectionRequest(DjangoCassandraModel):
  id = columns.BigInt(primary_key=True)
  from_user_id = columns.BigInt()
  to_user_id = columns.BigInt()
  created_at = columns.DateTime()
  updated_at = columns.DateTime()

  def save(self):
    if not self.id:
      self.id = generate_id()
    super().save()

  def __str__(self):
    return f"SuperConnectionRequest from {self.from_user_id} to {self.to_user_id}"
  

class Message(DjangoCassandraModel):
   id = columns.BigInt(primary_key=True)
   sender_id = columns.BigInt()
   receiver_id = columns.BigInt()
   message = columns.Text()
   created_at = columns.DateTime()
   updated_at = columns.DateTime()

   def save(self):
     if not self.id:
       self.id = generate_id()
     super().save()

   def __str__(self):
     return f"Message between {self.sender_id} and {self.receiver_id}"
   
class Chat(DjangoCassandraModel):
  id = columns.BigInt(primary_key=True)
  participants = columns.List(columns.BigInt())
  created_at = columns.DateTime()
  updated_at = columns.DateTime()

  def save(self):
    if not self.id:
      self.id = generate_id()
    super().save()

  def __str__(self):
    return f"Chat between {self.participants}"
    