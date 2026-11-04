
# Exigences de sécurité — Application des notes

| # | Le système doit… | Vérification | Étape du SDLC | Test |
|---|---|---|---|---|
| 1 | Empêcher un étudiant de modifier les notes. | Vérifier qu'une demande de modification par un étudiant est refusée. | Tests de sécurité | S3 |

| 2 | Exiger une authentification valide avant toute modification des notes. | Vérifier qu'une requête sans jeton d'authentification est refusée. | Tests de sécurité | S2 |

| 3 | Autoriser uniquement les enseignants et les administrateurs à modifier les notes. | Vérifier qu'un utilisateur avec le rôle étudiant reçoit un refus d'accès. | Tests de sécurité | S3, S4 |

| 4 | Vérifier que la nouvelle note est comprise entre 0 et 20 avant de l'enregistrer. | Tester une note invalide, comme -5 ou 25, et vérifier que la modification est refusée. | Tests de sécurité | S5 |

| 5 | Utiliser des requêtes SQL paramétrées pour empêcher les injections SQL. | Vérifier qu'une saisie contenant du code SQL malveillant ne modifie pas la base de données. | Tests de sécurité | S1 |


| 6 | Protéger les jetons d'authentification et ne jamais les publier dans le dépôt Git. | Vérifier que jetons.json est ignoré par Git. | Développement et tests de sécurité | Vérification Git (.gitignore) |


| 7 | Permettre à un enseignant de modifier uniquement les notes des étudiants de son module. | Vérifier qu'un enseignant autorisé peut modifier une note et que la nouvelle valeur est enregistrée. | Tests de sécurité | S6 |

| 8 | Ne jamais afficher les détails techniques des erreurs aux utilisateurs. | Vérifier qu'une erreur du serveur retourne le code 500 sans divulguer les informations de la base de données. | Tests de sécurité | S7 |
