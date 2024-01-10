# Amebo-drf

## Project Goals

This project is the Django Rest Framework API for the [Amebo React web app](https://github.com/sategie/Amebo). 

It is designed to provide JSON data to the Amebo React web app.

## Data Models

An Entity Relationship Diagram (ERD) was created and it is used to show the relationships between the database models.

The relationships between the models are explained in terms of cardinality .i.e minimums and maximums .e.g What is the mimimum number of model A that can be associated with a single instance of model B, and what is the maximum number of model A that can be associated with a single instance of model B.

The cardinality is then reversed between model B and model A .i.e What is the minimum number of model B that can be associated with a single instance of model A, and what is the maximum number of model B that can be associated with a single instance of model A.

A total of 6 models were designed for this project (exluding the built-in User model which Django provides by default).

The custom models are explained below:

### **Profile**

This represents the profile of the user in the database.
If the user associated with the profile is deleted, the corresponding profile is also deleted.
This model has the following fields:

**user**: This has one to one relationship with the User model meaning that a user can only have one profile and one profile can only have one user

**name**: This represents the name of the user and can be left blank if no name is provided

**created_date**: A DateTime field showing when the profile was created

**image**: This represents the profile picture of the user. If no profile picture is uploaded, a default profile picture is used

### **Post**

This is the database model which stores the posts a user creates in the application.
If the user(author of the post) is deleted, so also are the posts associated with the user.
The model contains the following fields:

**user**: This has a foreign key relationship with the User model and represents the author of the post.

**title**: This represents the title of the post

**post_content**: This represents the content of the post

**image**: This is an image field which handles how/where images are stored in the database. This field is not compulsory when creating a post .i.e null = True

**created_date**: A DateTime field showing when the post was created

**updated_date**: A DateTime field showing when the post was updated

### **Comment**

This represents the comments on a particular post.
If the user who created the comment is deleted, so also is the comment of the user.
If the post associated with the comment is deleted, so also is the comment.
The model has the following fields:

**user**: This has a foreign key relationship with the User model and represents the author of the comment

**post**: This has a foreign key relationship with the Post model and represents the post which is commented on

**comment_content**: This is a Text field which represents the actual content of the comment

**created_date**: A DateTime field showing when the comment was created

**updated date**: A DateTime field showing when the comment was updated

### **Like**

This represents the likes of a particular post.
This model has the following fields:

**user**: This has a foreign key relationship with the User model

**post**: This has a foreign key relationship with the Post model

**created_date**: A DateTime field showing when the like occurred

### **Follower**

The follower model is used to represent the relationship when one user follows another user.
It is set up so that you are not able to follow the same person twice and if the user is deleted, the associated follow relationship is also removed.
This model has the following fields:

**user**: This has a foreign key relationship with the User model and is used to represent the followers of the logged in user

**followed_user**: This also has a foreign key relationship with the User model and is used to represent the users who the logged in user is following

**created_date**: A DateTime field showing when the follow occurred

### **Notification**

The notification model is used to store messages for users. If a user is deleted, so also is the notification.
This model has the following fields:

**user**: This has a foreign key relationship with the User model. It has a related name 'notifications' which is used to specify the name of the reverse relationship from the default User model back to the Notification model

**message**: The message field is a Charfield which stores the message content of the notification

**created_date**: This is a DateTime field which records the date and time the notification was created

**seen**: This is a Boolean field which changes from the default 'false' to 'true' when a user sees the notification

