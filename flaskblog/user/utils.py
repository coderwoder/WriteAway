from flaskblog import mail
from flask import url_for,current_app
from flask_mail import Message

from PIL import Image
import os,secrets

def save_img(form_img,old_img):
    random_hex=secrets.token_hex(8)
    _,img_ext=os.path.splitext(form_img.filename)
    image_fn=random_hex+img_ext
    image_path= os.path.join(current_app.root_path,'static/profile pics',image_fn)

    # Save Space!!!!
    image_size=(131,131)
    i =Image.open(form_img)
    i.thumbnail(image_size)
    i.save(image_path)

    # delete the previous img if the user uploads the new successfully exp->default.png
    if old_img != 'default.png':
        old_path=os.path.join(current_app.root_path,'static/profile pics',old_img)
        if os.path.exists(old_path):
            os.remove(old_path)

    return image_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f''' To Reset Your Email, Visit The Following Link:
    {url_for('reset_token', token=token, _external=True)}


    If You Did Not Make This Request Don't Do Anything Nothing Will Happen. 
    '''
    mail.send(msg)

