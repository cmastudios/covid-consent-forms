from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InstitutionNetwork(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.institution} :: {self.ip}"


class InstitutionEmail(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    email_suffix = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.institution} :: {self.email_suffix}"
