from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.template.base import token_kwargs
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin, StaffuserRequiredMixin, SelectRelatedMixin
from django.views.generic.base import View, ContextMixin, TemplateView
from Portal.models import Game, Userprofile, Portal, TypeValue, FieldValue
from django.views.generic import ListView, DetailView, FormView, UpdateView, View, CreateView
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin, StaffuserRequiredMixin, SelectRelatedMixin
from django.views.generic.base import TemplateView
from Forum.models import Post
from Portal.models import Game, Userprofile, CommentNews, CharacterAttribute
from PortalAdmin.forms import UserForm, GuildSettingsForm, EnrollmentSettingsForm, TableNameForm, DbEntryForm, \
    SuperPortalForm
from PortalEnrollment.models import EnrollmentSettings
from PortalRaid.models import Raid, OutRaid
from SuperPortal.models import GuildSettings, SuperPortal
import account.views


class SignupView(account.views.SignupView):
    template_name = "Administration/accounts/signup.html"
    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

    def update_profile(self, form):
        profile = self.created_user.user  # replace with your reverse one-to-one profile attribute
        profile.some_attr = "some value"
        profile.save()


class MenuView(object):

    def get_context_data(self, **kwargs):
        context = super(MenuView, self).get_context_data(**kwargs)
        if 'pk_game' in self.kwargs:
            context['pk_game'] = self.kwargs['pk_game']
        context['games'] = Game.objects.all()
        dbs = {}
        for game in context['games']:
            dbs[game.pk] = TypeValue.objects.filter(game=game)
        context['db_tables'] = dbs
        return context



# @test_context('Administration/index.html')
class AdminIndexView(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, TemplateView):
    template_name = 'Administration/index.html'

    def get(self, request, *args, **kwargs):

        if GuildSettings.objects.all().count() and SuperPortal.objects.all().count():

            return super(AdminIndexView, self).get(request, *args, **kwargs)

        elif GuildSettings.objects.all().count() and SuperPortal.objects.all().count() == 0:

            return HttpResponseRedirect(reverse('admin_superportal_create'))

        else:

            return HttpResponseRedirect(reverse('admin_guild_setting_create'))

# DEBUT GUILD SETTINGS

class AdminGuildSetting(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, DetailView):
    template_name = 'Administration/guild_settings_detail.html'
    model = GuildSettings
    pk_url_kwarg = 'pk'

class AdminGuildSettingCreate(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, CreateView):
    template_name = 'Administration/guild_settings_form.html'
    model = GuildSettings
    form_class = GuildSettingsForm
    success_url = reverse_lazy('admin_superportal_create')

class AdminSuperPortalCreate(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, CreateView):
        template_name = 'Administration/superportal_form.html'
        model = SuperPortal
        form_class = SuperPortalForm
        success_url = reverse_lazy('admin_index')

class AdminGuildSettingEdit(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, UpdateView):
    template_name = 'Administration/guild_settings_form.html'
    model = GuildSettings
    form_class = GuildSettingsForm
    success_url = reverse_lazy('admin_index')

# FIN GUILD SETTINGS

# DEBUT MEMBRES

class AdminMembersView(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, ListView):
    model = User
    template_name = 'Administration/users/user_list.html'

    def dispatch(self, request, *args, **kwargs):
        return super(AdminMembersView, self).dispatch(request, *args, **kwargs)


class AdminUserDetailView(LoginRequiredMixin, StaffuserRequiredMixin, SelectRelatedMixin, MenuView, DetailView):
    template_name = 'Administration/users/user_detail.html'
    model = User
    select_related = ['userprofile']
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(AdminUserDetailView, self).get_context_data(**kwargs)
        context['participation'] = self.get_participation()
        return context

    def get_participation(self):
        list_out_raid = OutRaid.objects.all()
        participation = 0
        for character in self.object.charactermodel_set.all():
            for out_raid in list_out_raid:
                if out_raid.check_character_in(character):
                    participation += 1
        tmp = (participation * 100) / len(list_out_raid)
        return tmp

class AdminUserUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, UpdateView):
    template_name = 'Administration/users/user_edit_detail.html'
    model = Userprofile
    fields = ['birthday_date', 'gender', 'job_study', 'status', 'country', 'town', 'image_profile']
    template_name_suffix = '_update_form'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('admin_user_detail', kwargs={'pk': self.object.user.pk})


class LastPostLastComments(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax() and request.user in User.objects.all():
            choices = {
                'posts': list(Post.objects.filter(creator__pk=kwargs['pk']).order_by('created').values("body", "pk")[:10]),
                'comments': list(CommentNews.objects.filter(user__pk=kwargs['pk']).order_by('published_date').values('content',
                                                                                                                     'news__title',
                                                                                                                     'news_id')[:10]),
                'participation' : request.user.userprofile.get_participation_for_raids()
            }
            return JsonResponse(choices, safe=False)
# FIN MEMBRES

# DEBUT PORTAL
class AdminPortalCreateView(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, CreateView):
    model = Portal
    template_name = 'Administration/games/game_add.html'
    fields = ['portal', 'guild_name', 'active', 'name', 'image']

    def form_valid(self, form):
        form.instance.game = Game.objects.get(pk=self.kwargs['pk_game'])
        form.instance.guild_name = GuildSettings.objects.all().first().guild_name
        form.save()


class AdminPortalUpdate(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, UpdateView):
    model = Portal
    pk_url_kwarg = "pk_game"
    fields = ['portal', 'game', 'active', 'name', 'guild_name', 'image']
    template_name = 'Administration/portals/portal_form.html'

    def get_queryset(self):
        # get_object_or_404(self.model, game_id=self.kwargs['pk_game'])
        query = self.model.objects.filter(game__id=self.kwargs['pk_game'])
        return query
# FIN PORTAL

# DEBUT GAME


class AdminGamesView(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, ListView):
    model = Game
    template_name = 'Administration/games/game_list.html'


class AdminGameDetailView(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, DetailView):
    model = Game
    template_name = 'Administration/games/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AdminGameDetailView, self).get_context_data(**kwargs)
        return context

class AdminGameCreate(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, CreateView):
    model = Game
    template_name = 'Administration/games/game_add.html'
    fields = ['name', 'image', 'url_api']

    def get_success_url(self):
        return reverse_lazy('admin_portal_add', kwargs={'pk_game': self.kwargs['pk']})

    def form_valid(self, form):
        game = form.save()
        self.kwargs['pk'] = game.id
        Portal(portal=SuperPortal.objects.first(), game=game, name=game, guild_name=GuildSettings.objects.first(), image=game.image).save()
        return super(AdminGameCreate, self).form_valid(form)


class AdminGameUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, UpdateView):
    template_name = 'Administration/games/game_edit_detail.html'
    model = Game
    pk_url_kwarg = 'pk'
    fields = ['name', 'image', 'url_api']
    template_name_suffix = '_update_form'

# DEBUT GAME CHARACTERS

class AdminGameCharactersCreate(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, CreateView):
    model = CharacterAttribute
    template_name = 'Administration/games/add_character_attibutes.html'
    fields = ['attribute_name', 'attribute_value']

    def form_valid(self, form):

        form.instance.for_game = Game.objects.get(id=self.kwargs['pk'])
        form.save()
        return super(AdminGameCharactersCreate, self).form_valid(form)

# FIN GAME CHARACTERS

# FIN GAMES

# DEBUT ENROLLMENT

class AdminEnrollmentNeeds(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, CreateView):

    form_class = EnrollmentSettingsForm
    template_name = 'Administration/games/enrollment/needs.html'

    def get_context_data(self, **kwargs):

        context = super(AdminEnrollmentNeeds, self).get_context_data(**kwargs)
        context['needs'] = EnrollmentSettings.objects.filter(game_choice_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.game = Game.objects.get(id=self.kwargs['pk'])
        form.save()
        return super(AdminEnrollmentNeeds, self).form_valid(form)

# FIN ENROLLMENT

# DEBUT DATABASE

class AdminDatabaseAddTable(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, CreateView):

    form_class = TableNameForm
    template_name = 'Administration/games/database/add_table.html'

    def form_valid(self, form):
        form.instance.game = Game.objects.get(id=self.kwargs['pk_game'])
        form.save()
        self.success_url = reverse_lazy('admin_games_add_entry', kwargs={'pk_game': self.kwargs['pk_game'], 'pk_table': form.instance.id})
        return super(AdminDatabaseAddTable, self).form_valid(form)

class AdminDatabaseAddEntry(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, CreateView):
        form_class = DbEntryForm
        template_name = 'Administration/games/database/add_entry.html'

        def get_context_data(self, **kwargs):
            context = super(AdminDatabaseAddEntry, self).get_context_data(**kwargs)
            context['table'] = TypeValue.objects.get(pk=self.kwargs['pk_table'])
            context['entries'] = CharacterAttribute.objects.filter(for_game_id=self.kwargs['pk_game'], attribute_name=context['table'])
            return context

        def form_valid(self, form):
            form.instance.game = Game.objects.get(id=self.kwargs['pk_game'])
            form.save()
            CharacterAttribute(for_game_id=self.kwargs['pk_game'], attribute_name_id=self.kwargs['pk_table'], attribute_value_id=form.instance.pk).save()
            return super(AdminDatabaseAddEntry, self).form_valid(form)

        def get_success_url(self):
            return reverse_lazy('admin_games_add_entry', kwargs={'pk_game': self.kwargs['pk_game'], 'pk_table': self.kwargs['pk_table']})


class AdminEditEntry(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, UpdateView):
    template_name = 'Administration/games/database/edit_entry.html'
    model = FieldValue
    form_class = DbEntryForm
    pk_url_kwarg = 'pk_entry'

    def get_success_url(self):
        return reverse_lazy('admin_games_add_entry', kwargs={'pk_game': self.kwargs['pk_game'], 'pk_table': self.kwargs['pk_table']})

# FIN DATABASE

# DEBUT RAIDS

class AdminRaidsView(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, ListView):
    model = Raid
    template_name = 'Administration/raids/raid_list.html'

    def get_context_data(self, **kwargs):
        context = super(AdminRaidsView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        query = self.model.objects.filter(game__id=self.kwargs['pk_game'])
        return query


class AdminRaidsAdd(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, CreateView):
    model = Raid
    template_name = 'Administration/raids/raid_add.html'
    fields = ['name', 'lvl', 'number_of_boss', 'boss_successful', 'image']

    def get_success_url(self):
        return reverse('admin_raids', kwargs={'pk_game': self.kwargs['pk_game']})

    def form_valid(self, form):
        form.instance.game = Game.objects.get(id=self.kwargs['pk_game'])
        form.save()
        return super(AdminRaidsAdd, self).form_valid(form)


class AdminRaidsUpdate(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, UpdateView):
    model = Raid
    pk_url_kwarg = 'pk_raid'
    template_name = 'Administration/raids/raid_update.html'
    fields = ['name', 'lvl', 'number_of_boss', 'boss_successful', 'image']

    def get_success_url(self):
        return reverse('admin_raids', kwargs={'pk_game': self.kwargs['pk_game']})

    def form_valid(self, form):
        form.instance.game = Game.objects.get(id=self.kwargs['pk_game'])
        form.save()
        return super(AdminRaidsUpdate, self).form_valid(form)

class AdminRaidsDelete(LoginRequiredMixin, SuperuserRequiredMixin, MenuView, DeleteView):
    model = Raid
    template_name = 'Administration/raids/raid_delete_confirmation.html'
    pk_url_kwarg = 'pk_raid'


    def get_success_url(self):
        return reverse('admin_raids', kwargs={'pk_game': self.kwargs['pk_game']})
 # FIN RAID

# DEBUT RAID OUT
class AdminRaidOutView(LoginRequiredMixin, StaffuserRequiredMixin, MenuView, ListView):
    model = OutRaid
    template_name = 'Administration/raids/raidout_list.html'

    def get_queryset(self):
        query = self.model.objects.filter(raid__game_id=self.kwargs['pk_game'])
        return query


# FIN RAID OUT