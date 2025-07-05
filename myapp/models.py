from django.db import models


# --------------------- UTILISATEUR DE BASE ---------------------
from django.db import models
from django.utils.translation import gettext_lazy as _

# Enums
class NiveauAcces(models.TextChoices):
    SUPER_ADMIN = 'super_admin', _('Super Admin')
    GESTION_CONTENU = 'gestion_contenu', _('Gestion Contenu')
    GESTION_UTILISATEURS = 'gestion_utilisateurs', _('Gestion Utilisateurs')

class ContenuStatut(models.TextChoices):
    BROUILLON = 'brouillon', _('Brouillon')
    EN_ATTENTE = 'en_attente', _('En attente')
    VALIDE = 'valide', _('Validé')
    REJETE = 'rejete', _('Rejeté')

class VersionStatut(models.TextChoices):
    EN_COURS = 'en_cours', _('En cours')
    ARCHIVEE = 'archivee', _('Archivée')

class ModificationStatut(models.TextChoices):
    PROPOSEE = 'proposee', _('Proposée')
    ACCEPTEE = 'acceptee', _('Acceptée')
    REFUSEE = 'refusee', _('Refusée')

class HistoriqueStatut(models.TextChoices):
    INFO = 'info', _('Info')
    AVERTISSEMENT = 'avertissement', _('Avertissement')
    CRITIQUE = 'critique', _('Critique')

class WorkflowStatut(models.TextChoices):
    ACTIF = 'actif', _('Actif')
    INACTIF = 'inactif', _('Inactif')

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Employe(Utilisateur):
    departement = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} - {self.departement}"

class ServiceOrganisation(Utilisateur):
    secteurResponsable = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} - {self.secteurResponsable}"

class Administrateur(Utilisateur):
    niveau_acces = models.CharField(
        max_length=30,
        choices=NiveauAcces.choices,
        default=NiveauAcces.GESTION_CONTENU,
    )

    def __str__(self):
        return f"{self.nom} - {self.niveau_acces}"

class Contenu(models.Model):
    titre = models.CharField(max_length=200)
    corps = models.TextField()
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    statut = models.CharField(
        max_length=20,
        choices=ContenuStatut.choices,
        default=ContenuStatut.BROUILLON
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Version(models.Model):
    contenu = models.ForeignKey(Contenu, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=VersionStatut.choices,
        default=VersionStatut.EN_COURS
    )

class Modification(models.Model):
    contenu = models.ForeignKey(Contenu, on_delete=models.CASCADE)
    description = models.TextField()
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_modification = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=ModificationStatut.choices,
        default=ModificationStatut.PROPOSEE
    )

class Commentaire(models.Model):
    contenu = models.ForeignKey(Contenu, on_delete=models.CASCADE)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    texte = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)

class Historique(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    action = models.TextField()
    date_action = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=HistoriqueStatut.choices,
        default=HistoriqueStatut.INFO
    )

class WorkflowValidation(models.Model):
    nom = models.CharField(max_length=100)
    statut = models.CharField(
        max_length=20,
        choices=WorkflowStatut.choices,
        default=WorkflowStatut.ACTIF
    )

class EtapeValidation(models.Model):
    workflow = models.ForeignKey(WorkflowValidation, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    ordre = models.PositiveIntegerField()
