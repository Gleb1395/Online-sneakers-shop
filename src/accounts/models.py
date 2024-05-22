from datetime import datetime, date

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from faker import Faker
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import ClientManager


class Client(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("name"), max_length=150, blank=True)
    last_name = models.CharField(_("surname"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    phone_number = PhoneNumberField(_("phone number"), null=True, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateField(_("birth date"), blank=True, null=True)
    photo = models.ImageField(_("photo"), blank=True, null=True, upload_to="media/img/")
    objects = ClientManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_registration_age(self):
        return f"Time on site: {timezone.now() - self.date_joined}"

    @classmethod
    def create_client(cls, count) -> None:
        faker = Faker()
        for i in range(count):
            client = Client.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                phone_number=faker.phone_number(),
                date_joined=faker.date_between(start_date=date(2020, 5, 13),
                                               end_date=date(2023, 5, 13)),
                birth_date=faker.date_of_birth(minimum_age=16, maximum_age=60),
            )
            client.save()
