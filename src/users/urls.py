from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (LoginView, RegisterView,
ResetPasswordView, ResetPasswordCompleteView,
PanelView, LogoutView, PanelChangePasswordView,
PanelEditAccountView, TicketListView, TicketDetailsView,
TicketCloseByUserView, TicketCreateView, BookmarksView, FavoriteView,
CommentView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-recovery/', ResetPasswordView.as_view(), name='password-recovery'),
    path('password-recovery-complete/<str:uidb64>/<str:token>', ResetPasswordCompleteView.as_view(), name='password-recovery-complete'),
    path('panel/', login_required(PanelView.as_view()), name='user-panel'),
    path('panel/change-password/', login_required(PanelChangePasswordView.as_view()), name='change-password'),
    path('panel/edit-account/', login_required(PanelEditAccountView.as_view()), name='user-edit-account'),
    path('panel/ticket/', login_required(TicketListView.as_view()), name='ticket-list'),
    path('panel/ticket/<int:id>/details', login_required(TicketDetailsView.as_view()), name='ticket-details'),
    path('panel/close-ticket/<int:id>/', login_required(TicketCloseByUserView.as_view()), name='ticket-close'),
    path('panel/create-ticket/', login_required(TicketCreateView.as_view()), name='ticket-create'),
    path('panel/bookmark/', login_required(BookmarksView.as_view()), name='bookmarks'),
    path('panel/favorite/', login_required(FavoriteView.as_view()), name='favorite'),
    path('panel/comments/', login_required(CommentView.as_view()), name='comments'),
    path('', include('users.api.urls')),
]