from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class CompletionReq(FlaskForm):
    # 必填，长度最大2000个字符
    query = StringField("query", validators=[DataRequired(message="请输入问题"), Length(max=2000, message="问题长度不能超过2000个字符")])
    