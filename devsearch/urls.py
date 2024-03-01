from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import customers, authors, users


urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('user/', include('users.urls')),
    path('rooms/', include('chatrooms.urls')),
    path('', include('blogwcss.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/author/', authors.RegisterAuthor.as_view(), name='author_register'),
    path('accounts/register/customer/', customers.RegisterUser.as_view(), name='customer_register'),
    path('accounts/signup/', users.SignUpView.as_view(), name='signup'),
    path('edit-account/customer/', customers.EditCustomerAccount, name="edit-account"),
    path('edit-account/author/', authors.EditAuthorAccount, name="edit-author-account"),
    path('account/author/', authors.authorAccount, name="author-account"),
    path('account/customer/', customers.customerAccount, name="customer-account"),



]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




# 1 - User submits email for reset              //PasswordResetView.as_view()           //name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view()        //name="passsword_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfirmView()            //name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView.as_view()   //name="password_reset_complete"
