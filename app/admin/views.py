# coding:utf-8
from flask_admin.contrib.mongoengine import ModelView
from wtforms import fields, widgets
from flask.ext.admin import AdminIndexView, expose, helpers
from flask.ext.login import current_user, login_user, logout_user
from flask import redirect, url_for, request
from forms import LoginForm


class AdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('.login'))
        return super(AdminIndexView, self).index()

    @expose('/login', methods=('GET', 'POST'))
    def login(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = form.get_user()
            login_user(user)
            redirect(url_for('.index'))

        self._template_args['form'] = form

        return super(AdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


# Define wtforms widget and field
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class UserView(ModelView):
    can_create = False
    can_delete = False
    column_display_pk = True
    column_filters = ('name', 'email')

    edit_template = 'admin/edit_user.html'
    form_overrides = dict(description=CKTextAreaField)

    form_columns = ('name', 'email', 'description')

    def is_accessible(self):
        return current_user.is_authenticated()


class PostView(ModelView):

    column_display_pk = True

    form_overrides = dict(content=CKTextAreaField)
    create_template = 'admin/create_post.html'
    edit_template = 'admin/edit_post.html'

    column_list = ('id', 'title', 'content', 'author', 'tags', 'status', 'create_time', 'modify_time')
    # column_labels = dict(id='ID',
    #                      title=u'标题',
    #                      content=u'内容',
    #                      author=u'作者',
    #                      tags=u'标签',
    #                      status=u'状态',
    #                      create_time=u'创建时间',
    #                      modify_time=u'修改时间')

    column_choices = {
        'status': [
            (0, 'draft'),
            (1, 'published')
        ]
    }

    column_filters = ('title',)

    column_searchable_list = ('content',)

    column_sortable_list = ('create_time', 'modify_time')

    def is_accessible(self):
        return current_user.is_authenticated()



