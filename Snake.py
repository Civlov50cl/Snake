import pygame
import sys
import random
import os

pygame.init()

taille_fenetre = (800, 600)
fenetre = pygame.display.set_mode(taille_fenetre)

pygame.display.set_caption("Jeu Snake")

horloge = pygame.time.Clock()

serpent = [(200, 200), (210, 200), (220, 200)]
direction = "droite"

def creer_pomme(serpent):
    while True:
        x = random.randint(0, taille_fenetre[0] // 10 - 1) * 10
        y = random.randint(0, taille_fenetre[1] // 10 - 1) * 10
        pomme = (x, y)
        if pomme not in serpent:
            return pomme

pomme = creer_pomme(serpent)
score = 0
police = pygame.font.Font(None, 36)

meilleur_score = 0
meilleur_joueur = ""

if os.path.exists("meilleur_score.txt"):
    with open("meilleur_score.txt", "r") as f:
        meilleur_score = int(f.readline().strip())  
        meilleur_joueur = f.readline().strip()  

nouveau_meilleur_score = False
def afficher_game_over(fenetre, score, meilleur_score, meilleur_joueur ):
    police_game_over = pygame.font.Font(None, 72)
    texte_game_over = police_game_over.render("Game Over", True, (255, 255, 255))
    texte_score = police.render(f"Score : {score}", True, (255, 255, 255))
    texte_meilleur_score = police.render(f"Meilleur score : {meilleur_score} ({meilleur_joueur})", True, (255, 255, 255))
    texte_rejouer = police.render("Appuyez sur R pour rejouer ou Echap pour quitter", True,(255, 255, 255))
    fenetre.blit(texte_game_over, (taille_fenetre[0] // 2 - texte_game_over.get_width() // 2, taille_fenetre[1] // 2 - texte_game_over.get_height() // 2))
    fenetre.blit(texte_score, (taille_fenetre[0] // 2 - texte_score.get_width() // 2, taille_fenetre[1] // 2 + texte_game_over.get_height() // 2))
    fenetre.blit(texte_rejouer, (taille_fenetre[0] // 2 - texte_rejouer.get_width() // 2, taille_fenetre[1] // 2 + texte_game_over.get_height() + texte_score.get_height() + texte_meilleur_score.get_height()))
    fenetre.blit(texte_meilleur_score, (taille_fenetre[0] // 2 - texte_meilleur_score.get_width() // 2, taille_fenetre[1] // 2 + texte_game_over.get_height() + texte_score.get_height()))

def creer_obstacles(nombre_obstacles, serpent, pomme):
    obstacles = []
    while len(obstacles) < nombre_obstacles:
        x = random.randint(0, taille_fenetre[0] // 10 - 1) * 10
        y = random.randint(0, taille_fenetre[1] // 10 - 1) * 10
        obstacle = (x, y)
        if obstacle not in serpent and obstacle != pomme and obstacle != (200, 200) and obstacle != (210, 200) and obstacle != (220, 200):
            obstacles.append(obstacle)
    return obstacles



def demander_nom_joueur():
    pygame.display.set_caption("Entrez votre nom")
    nom_joueur = ""
    police = pygame.font.Font(None, 36)
    en_cours = True
    afficher_texte = True

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    en_cours = False
                    afficher_texte = False
                elif event.key == pygame.K_BACKSPACE:
                    nom_joueur = nom_joueur[:-1]
                else:
                    nom_joueur += event.unicode

        fenetre.fill((0, 0, 0))
        if afficher_texte:
            texte_felicitations = police.render("Félicitations, tu as battu le record. Entre ton nom :", True, (255, 255, 255))
            texte_nom = police.render(f"Nom: {nom_joueur}", True, (255, 255, 255))
            fenetre.blit(texte_felicitations, (taille_fenetre[0] // 2 - texte_felicitations.get_width() // 2, taille_fenetre[1] // 2 - texte_felicitations.get_height()))
            fenetre.blit(texte_nom, (taille_fenetre[0] // 2 - texte_nom.get_width() // 2, taille_fenetre[1] // 2))
        
        pygame.display.flip()
    
    pygame.display.set_caption("Jeu Snake")
    return nom_joueur



def afficher_ecran_demarrage(fenetre):
    police_demarrage = pygame.font.Font(None, 72)
    texte_demarrage = police_demarrage.render("Jeu Snake", True, (255, 255, 255))
    texte_commandes = police.render("Utilisez les flèches pour jouer", True, (255, 255, 255))
    texte_appuyez = police.render("Appuyez sur une flèche pour commencer", True, (255, 255, 255))
    fenetre.blit(texte_demarrage, (taille_fenetre[0] // 2 - texte_demarrage.get_width() // 2, taille_fenetre[1] // 2 - texte_demarrage.get_height() // 2))
    fenetre.blit(texte_commandes, (taille_fenetre[0] // 2 - texte_commandes.get_width() // 2, taille_fenetre[1] // 2 + texte_demarrage.get_height() // 2))
    fenetre.blit(texte_appuyez, (taille_fenetre[0] // 2 - texte_appuyez.get_width() // 2, taille_fenetre[1] // 2 + texte_demarrage.get_height() + texte_commandes.get_height()))


game_over = False
ecran_demarrage = True
en_cours = True

while en_cours:
    if ecran_demarrage:
        fenetre.fill((0, 0, 0))
        afficher_ecran_demarrage(fenetre)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                ecran_demarrage = False
                nombre_obstacles = 10
                obstacles = creer_obstacles(nombre_obstacles, serpent, pomme)

    elif not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "droite":
                    direction = "gauche"
                if event.key == pygame.K_RIGHT and direction != "gauche":
                    direction = "droite"
                if event.key == pygame.K_UP and direction != "bas":
                    direction = "haut"
                if event.key == pygame.K_DOWN and direction != "haut":
                    direction = "bas"

        tete = serpent[0]
        x, y = tete
        if direction == "gauche":
            x -= 10
        elif direction == "droite":
            x += 10
        elif direction == "haut":
            y -= 10
        elif direction == "bas":
            y += 10
        nouvelle_tete = (x, y)

        if (x < 0 or x >= taille_fenetre[0] or y < 0 or y >= taille_fenetre[1] or nouvelle_tete in serpent[1:] or nouvelle_tete in obstacles) and score != 0:
            game_over = True

        else:
            serpent.insert(0, nouvelle_tete)
            serpent.pop()

        if tete == pomme:
            score += 1
            if score > meilleur_score:
                meilleur_score = score
                nouveau_meilleur_score = True
                meilleur_joueur = "TOI !!!"
                with open("meilleur_score.txt", "w") as f:
                    f.write(str(meilleur_score))
            pomme = creer_pomme(serpent)
            serpent.append(serpent[-1])

        fenetre.fill((0, 0, 0))

        for segment in serpent:
            pygame.draw.rect(fenetre, (0, 255, 0), (*segment, 10, 10))

        pygame.draw.rect(fenetre, (255, 0, 0), (*pomme, 10, 10))
        for obstacle in obstacles:
            pygame.draw.rect(fenetre, (0, 0, 255), (*obstacle, 10, 10))


        texte = police.render(f"Score: {score}", True, (255, 255, 255))
        fenetre.blit(texte, (10, 10))
        texte_meilleur_score = police.render(f"Meilleur score : {meilleur_score} ({meilleur_joueur})", True, (255, 255, 255))
        fenetre.blit(texte_meilleur_score, (10, 50))


        pygame.display.flip()
        horloge.tick(15 + score)
    else:
        if nouveau_meilleur_score:
            nom_joueur = demander_nom_joueur()
            meilleur_score = score
            meilleur_joueur = nom_joueur
            with open("meilleur_score.txt", "w") as f:
                f.write(f"{meilleur_score}\n{meilleur_joueur}")
            nouveau_meilleur_score = False

        afficher_game_over(fenetre, score, meilleur_score, meilleur_joueur)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                en_cours = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_over = False
                score = 0
                serpent = [(200, 200), (210, 200), (220, 200)]
                direction = "droite"
                pomme = creer_pomme(serpent)
                nombre_obstacles = 10
                obstacles = creer_obstacles(nombre_obstacles, serpent, pomme)



pygame.quit()
sys.exit()
