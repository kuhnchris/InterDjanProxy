from django.db import models
from django.contrib.auth.models import Permission


class menuItem(models.Model):
    description = models.CharField(max_length=100)
    href = models.CharField(max_length=255)
    requiresLogin = models.BooleanField(default=True)
    onlyDisplayIfLoggedOut = models.BooleanField(default=False)
    requiredPermissions = models.ForeignKey(blank=True, null=True, to=Permission, on_delete=models.deletion.DO_NOTHING)

    def __str__(self):
        return f'{self.description} ({self.href}), displayed for: OnlyLoggedOut? {self.onlyDisplayIfLoggedOut} - LoggedIn? {self.requiresLogin} - Permission {self.requiredPermissions}'

class portalItem(menuItem):
    pass
