# Spurtresultat

#### Discord bot för att jämföra spurttider på orienterings-tävlingar (inom en klubb)

## Funktionalitet

!Hej --> Hej \<namn>

!Hjälp --> List på kommandon

!Res <tävlingsID> --> Topp tio bästa spurttider i klubben för tävling

!Sök <tävling> --> Lista på tävlingar och dess Id:n

## Konfigurering (config.py)

Nycklar sparas som systemvariabler, namn skrivs in i config.py De som behövds är api nyckel till eventor och token till discord bot.

"organisationid" är klubbens id

"downloadsPath" mapp där nedladdade resultat sparas

## Resurser

- https://eventor.orientering.se/Documents/Guide_Eventor_-_Hamta_data_via_API.pdf

- https://eventor.orientering.se/api/documentation