from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError('Author name cannot be Empty')
             
    
        existing_author=Author.query.filter(Author.name == name).first()
        if existing_author:
            raise ValueError('No two Authors can have the same name') 
        return name
    

    @validates('phone_number')
    def validate_phone_number(self,key,phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('Author phone numbers must be 10 digits')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('content')
    def validate_content(self,key,content):
        if len(content) < 250:
            raise ValueError('Content must have at least 250 characters')
        return content
 
    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary) > 250:
            raise ValueError('Summary must have a maximum of 250 characters')
        return summary

    @validates('category')
    def validate_category(self,key,category):
        if category not in ['Fiction', 'Non-Fiction']: 
            raise ValueError('category should be either Fiction or Non-Fiction')
        return category
    
    @validates('title')
    def validate_title(self,key,title):
        clickbait_words = ['Won\'t Believe','Secret','Top','Guess']
        if not any (word in title for word in clickbait_words):        
            raise ValueError("Title must contain one of the following: Won't Believe,Secret,Top,Guess")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
