# from extensions import db


# class Model(db.Model):
# 	__tablename__ = 'table_name'
#     __table_args__ = {"schema": "schema_name",'extend_existing': True}

#     id = db.Column(db.String(255), primary_key=True)
#     user_message = db.Column(db.Text)
#     system_instructions = db.Column(db.Text)
#     bot_message = db.Column(db.Text)
#     completion_tokens = db.Column(db.Integer)
#     prompt_tokens = db.Column(db.Integer)
#     finish_reason = db.Column(db.String(255))
#     model = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime)
#     updated_at = db.Column(db.DateTime)
#     def __repr__(self):
#         return f'<Message {self.id}>'
