
## If you wanna install this project
virtualenv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Dans cette application , les fonctionnalités suivantes sont présentes : 
 - Un utilisateur peut :
  -créer un compte , soit via le side admin , soit via le site web .
  -Se connecter après avoir créer son propre compte.
  -Modifier ces informations de profil (soit depuis le site Admin, soit depuis le site web.
  -Consulter la liste des voitures présentes dans l'agence .
  -Voir la description de chaque voiture.
  -Rechercher une voiture
  -Faire une location de la voiture souhaitée.Il doit fournir ses informations , suivi de la date de location et la date de retour . Le montant total de la location est calculé à partir de la différence entre les deux dates fournies.
  -Annuler une location déjà faite .
  - Payer sa location ( à l'aide d'un API Stripe en ligne) 
 -L'adminitrateur possède le controle tolal de l'application , ainsi :
   -Il peut gérer les locations .
   -Ajouter de nouvelles voitures.
   -Ajouter des voitures en utilisant du web scrapping (Récupération des données de la voiture et les stocker dans la base de données ).
   -Ajouter des sections Faqs comme une assistance qui permettra aux utilisateurs de mieux utiliser l'application.
   -Ajouter les informations concernants l'agence, son emplacements , ses numéros de téléphone .
