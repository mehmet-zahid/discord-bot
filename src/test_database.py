from db_wrapper import MongoManager

db = MongoManager(db_name="discord", conn_str="mongodb://root:root@<ip>:27017")

test_data = {"data": "test"}

db.add_document(test_data, "discord")
  
db.show_all_documents("discord")

