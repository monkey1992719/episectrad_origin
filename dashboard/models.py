from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import int_list_validator

import structlog

logger = structlog.get_logger()

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        user = self.filter(email__iexact=username).first()
        if not user:
            raise User.DoesNotExist
        return user


class User(AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.EmailField(_("email address"), unique=True, blank=False)
    email_confirmed = models.BooleanField(blank=True, default=False)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    def get_full_name(self):
        if self.username:
            return self.username
        return self.email

    def get_short_name(self):
        if self.username:
            return self.username
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email


# chart models

class ChartString(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = "chart_strings"



# indicator models

class IndicatorInput(models.Model):
    parameter = models.CharField(max_length = 256)
    datatype = models.CharField(max_length = 256)

    class Meta:
        db_table = "indicator_input"

class Indicator(models.Model):
    name = models.CharField(max_length = 64)
    id_letter = models.CharField(max_length = 32)
    category = models.CharField(max_length = 32)
    value_indicator = models.IntegerField(default=0)
    possible_combine = models.IntegerField(default=0)
    combine_main = models.IntegerField(default=0)
    param_name = models.CharField(max_length = 32)
    indicatorinputs = models.ManyToManyField(IndicatorInput)

    class Meta:
        db_table = "indicators"


# plot model

class ChartPlot(models.Model):

    id = models.AutoField(primary_key=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    plottype = models.CharField(max_length = 30, default="Line")
    plotname = models.CharField(max_length = 256)
    setting_manual = models.IntegerField()

    class Meta:
        db_table = "chart_plot"


# must be filtered by user also
class ChartPlotSettingManager(models.Manager):
    def create_setting(self, user, plot, color, width, plottype):
        setting = self.create(user=user, plot=plot, color=color, width=width, plottype=plottype)
        setting.save(using=self._db)
        return setting

    # def update_setting(self, user, plot, color, width=1, plottype='Line'):
    def update_setting(self, plot, color, width=1, plottype='Line'):
        setting = self.filter(plot=plot).first()
        # setting = self.model(user=user, plot=plot)
        if setting is None:
            setting = self.create(plot=plot, color=color, width=width, plottype=plottype)
            # setting = self.create(user=user, plot=plot, color=color, width=width, plottype=plottype)
        else:
            setting.color = color
            setting.width = width
            setting.plottype = plottype
            setting.save()
            
        return setting

class ChartPlotDefaultSetting(models.Model):

    id = models.AutoField(primary_key=True)
    plot = models.OneToOneField(ChartPlot, on_delete=models.CASCADE)
    color = models.CharField(max_length = 30, default="#000000")
    width = models.IntegerField(default=1)
    plottype = models.CharField(max_length = 30, default="Line")

    class Meta:
        db_table = "chart_plot_default_setting"

class ChartPlotSetting(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plot = models.OneToOneField(ChartPlot, on_delete=models.CASCADE)
    color = models.CharField(max_length = 30, default="#000000")
    width = models.IntegerField(default=1)
    plottype = models.CharField(max_length = 30, default="Line")

    objects = ChartPlotSettingManager()

    class Meta:
        db_table = "chart_plot_setting"

# trade setting models

class TradeIndicator(models.Model):
    BACKTEST_MODE = (
        (0, 'Traditional'),
        (1, 'Threshold'),
        (2, 'Change Direction'),
        (3, 'Cross with Other'),
        (4, 'Cross with Inverted'),
        (5, 'Value Set'),
        (6, 'Time Set')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    backtest_mode = models.IntegerField(default = 0, choices = BACKTEST_MODE)
    with_main = models.IntegerField(default = 0)
    signal = models.IntegerField(default = 0)

    def tradchoice(self):
        if self.tradeindicatorindicator_set.filter(indicator__value_indicator=0).count() > 0:
            return 1
        return 0

    def title(self):
        return '<br>'.join([tii.indicator.name for tii in self.tradeindicatorindicator_set.all()])

    def title1(self):
        return ','.join([tii.indicator.name for tii in self.tradeindicatorindicator_set.all()])

    def __str__(self):
        return ','.join([tii.indicator.name for tii in self.tradeindicatorindicator_set.all()])

    class Meta:
        db_table = "trade_indicator"


class TradeIndicatorIndicator(models.Model):
    trade_indicator = models.ForeignKey(TradeIndicator, on_delete=models.CASCADE)
    indicator = models.OneToOneField(Indicator, on_delete=models.CASCADE)
    traditional = models.IntegerField(default=0)

    def __str__(self):
        return self.indicator.name

    class Meta:
        db_table = "trade_indicator_indicator"


class TradeIndicatorPlotThreshold(models.Model):
    trade_indicator_indicator = models.ForeignKey(TradeIndicatorIndicator, on_delete=models.CASCADE)
    plot = models.OneToOneField(ChartPlot, on_delete=models.CASCADE)
    threshold_b = models.FloatField(default = 0.0)
    threshold_s = models.FloatField(default = 0.0)

    class Meta:
        db_table = "trade_indicator_plot_threshold"


class TradeIndicatorCross2(models.Model):
    trade_indicator_indicator1 = models.OneToOneField(TradeIndicatorIndicator, on_delete=models.CASCADE, related_name='tii2tii1')
    chart_plot1 = models.OneToOneField(ChartPlot, on_delete=models.CASCADE, related_name='cp2cp1')
    trade_indicator_indicator2 = models.OneToOneField(TradeIndicatorIndicator, on_delete=models.CASCADE, related_name='tii2tii2')
    chart_plot2 = models.OneToOneField(ChartPlot, on_delete=models.CASCADE, related_name='cp2cp2')

    class Meta:
        db_table = "trade_indicator_cross2"


class TradeIndicatorCrossv(models.Model):
    trade_indicator_indicator = models.OneToOneField(TradeIndicatorIndicator, on_delete=models.CASCADE)
    chart_plot = models.OneToOneField(ChartPlot, on_delete=models.CASCADE)

    class Meta:
        db_table = "trade_indicator_crossv"


class IndicatorInputValue(models.Model):
    trade_indicator_indicator = models.ForeignKey(TradeIndicatorIndicator, on_delete=models.CASCADE)
    indicator_input = models.OneToOneField(IndicatorInput, on_delete=models.CASCADE)
    value = models.CharField(max_length=32)

    class Meta:
        db_table = "indicator_input_value"


# dashboard model

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length = 16, default='GOLD')
    period = models.CharField(max_length = 16, default='36m')
    interval = models.CharField(max_length = 16, default='15min')
    bIntraday = models.IntegerField(default=0)
    enter_signal = models.IntegerField(default=0)
    title = models.CharField(max_length = 256, default='My Dashboard')

    class Meta:
        db_table = "dashboards"


class Backtest(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    mode = models.IntegerField(default=0)
    tradeindicator = models.OneToOneField(TradeIndicator, on_delete=models.CASCADE)
    pricebar_pattern = models.CharField(max_length = 128)
    chart_pattern = models.CharField(max_length = 128)
    attribute = models.IntegerField(default = 0)

    def title(self):
        if self.mode == 0:
            return self.tradeindicator.title1()
        elif self.mode == 1:
            return self.pricebar_pattern
        else:
            return self.chart_pattern

    class Meta:
        db_table = "backtests"