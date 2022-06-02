from pydoc import Doc
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from decrees.models import Position, Person, Event
from decrees.forms import EventForm, Event_form_for_Admin

# admin.site.register(Formats)
# admin.site.register(Document)
# admin.site.register(Subscription)


class EventLinline(admin.StackedInline):
    model = Event
    form = EventForm
    # exclude = ('line','full_text')
    readonly_fields = ['action', 'date', 'level', 'position']
    list_display = ('action',)
    show_change_link = True
    # raw_id_fields = ['action',] # many to many
    verbose_name = 'событие'
    verbose_name_plural = 'Назначения и отставки'
    can_delete = False
    extra = 0

    fieldsets = (
        (None, {
            'fields': ('action', 'level', 'date', 'position', 'line')
        }),
        ('Полный текст документа', {
            'classes': ('collapse',),
            'fields': ('full_text',),
            'description':'<h3>Текст</h3>'
        },
        
        ),
    )


class PersonAdmin(admin.ModelAdmin):
    
    # @admin.display(description='последняя должность')
    # def display_position(self, obj):
    #     return Event.objects.filter(person=obj)[0]
    # 'display_position'

    list_display = ('name',)
    inlines = [
        EventLinline
    ]
    
    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )

    # add_fieldsets =  (
    #     (None, {
    #         'fields': ('name', )
    #     }),
    # )


    # list_display_links = ('name', 'display_position')


class MyUsersAdmin(admin.ModelAdmin):
    # date_hierarchy = 'last_login'
    actions_on_top = False
    actions_on_bottom = True
    readonly_fields = ['username']
    
    # fields = ('username',('password', 'email'))
    # exclude = ['username']


    @admin.display(description='раскрашенное имя')
    def colored_name(self, obj):
        return format_html(
            '<span style="color: #{};">{}</span>',
            'FF5733',
            obj.username,
        )
    
    @admin.display()
    def get_formats(self, obj):
        return obj.username + '_modified_'

    list_display = ('username', 'get_formats', 'colored_name', 'location',)
    list_display_links = ('username',)
    list_editable = ('location', )
    list_filter = ('location',)
    
    
    fieldsets = (
        (None, {
            'fields': ('username', 'location')
        }),
        ('Еще опции', {
            'classes': ('extrapretty','collapse'),
            'fields': ('email','last_login'),
            'description':'<h3>хуй</h3>'
        },
        
        ),
    )


class MyEventAdmin(admin.ModelAdmin):
    # form = Event_form_for_Admin
    
    list_display = ['person', 'full_text', 'position']


    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('person', 'full_text',),
    #     }),
    # )


class MySubsAdmin(admin.ModelAdmin):
    filter_horizontal = ('user',)

# class YourModelAdmin(admin.ModelAdmin):
#         formfield_overrides = {
#             models.TextField: {'widget' : RichTextEditorWidget},
#         }

# admin.site.register(YourModel, YourModelAdmin)


# admin.site.register(MyUser, MyUsersAdmin)
# admin.site.unregister(Subscription) #First unregister the old class
# admin.site.register(Subscription, MySubsAdmin)

admin.site.register(Position)
# admin.site.register(Event)
admin.site.register(Person, PersonAdmin)
admin.site.register(Event, MyEventAdmin)



# admin.site.unregister(Token) #First unregister the old class
# admin.site.register(Token, AuthTokenAdmin)

# class MyUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = MyUser
#     list_display = ['username','email', 'location_2']
#     actions_selection_counter: bool = True
#     # date_hierarchy = 'last_login'   
    
#     # fieldsets = (
#     #     (None, {"fields": ("username", "password")}),
#     #     (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'location_2')}),
#     #     (
#     #         _("Permissions"),
#     #         {
#     #             "fields": (
#     #                     "is_active",
#     #                     "is_staff",
#     #                     "is_superuser",
#     #                     "groups",
#     #                     "user_permissions",
                        
             
#     #             ),
#     #         },
#     #     ),
#     # )

# admin.site.register(MyUser, MyUserAdmin)


