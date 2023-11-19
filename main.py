import subprocess

def verifyrequirement():
    try:
        with open('requirements.txt', 'r') as file:
            required_libraries = [line.strip() for line in file.readlines()]
        installed_libraries = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')
        missing_libraries = [lib for lib in required_libraries if lib not in installed_libraries]
        if missing_libraries:
            print("Bibliothèques manquantes détectées. Installation en cours...")
            for library in missing_libraries:
                subprocess.run(['pip', 'install', library])
            print("Installation terminée.")
        else:
            print("Toutes les bibliothèques nécessaires sont déjà installées.")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

try:          
    import sqlite3
    import webbrowser
    from colorama import Fore, Style
    import webview
except:
    verifyrequirement()


def main(utilisation):
    print("")
    print(Fore.GREEN + "Borne avec coordonnées")
    print(Fore.RED + "Borne avec adresse")
    print(Style.RESET_ALL)

    latitude = None
    longitude = None
    connexion = sqlite3.connect("bornes.db")
    curseur = connexion.cursor()    

    nombre = 1
    all_location = []
    ville =  input("Entrez la ville dans laquelle se situe votre borne : ")
    print("")
    curseur.execute(f'SELECT bornes.n_operateur, bornes.ad_station, bornes.accessibilité, bornes.puiss_max, bornes.Xlongitude, bornes.Ylatitude, code_insee_postal.CodePostal FROM bornes JOIN code_insee_postal ON bornes.code_insee = code_insee_postal.CodeINSEE where Commune like "{ville}"')
    for resultat in curseur:
        if resultat not in all_location:
            if resultat[4] == None and resultat[5] == None:
                print(Fore.RED + f"{nombre} | Adresse : {resultat[1]} | Opérateur : {resultat[0]} | Accessibilité : {resultat[2]} | Puissance : {resultat[3]}")
                print(Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"{nombre} | Adresse : {resultat[1]} | Opérateur : {resultat[0]} | Accessibilité : {resultat[2]} | Puissance : {resultat[3]}")
                print(Style.RESET_ALL)
            nombre += 1
            all_location.append(resultat)
    try :
        resultat[0]
        print(f"Voici toutes les bornes situés à {ville}, choisissez en une. ")
        rep = int(input("Chiffre : "))-1
        bonnombre = False
        while not bonnombre:
            try:
                if all_location[rep][4] == None and all_location[rep][5] == None:
                    adresse = all_location[rep][1]
                    if utilisation == 1:
                        webbrowser.open(f"https://www.google.com/maps/place/{adresse}")
                    elif utilisation == 2:
                        try:
                            webview.create_window("GoogleMaps",f'https://www.google.com/maps/place/{adresse}', width=1200, height=800)
                            print("Veuillez fermer la fenêtre pour continuer.")
                            webview.start()
                        except:
                            print("La page python n'a pas réussi à s'ouvrir", "\n", "Le page s'ouvre alors avec votre navigateur...")
                            webbrowser.open(f"https://www.google.com/maps/place/{adresse}")
                    bonnombre = True
                else:
                    longitude = all_location[rep][4]
                    latitude = all_location[rep][5]
                    if utilisation == 1:
                        webbrowser.open(f"https://www.google.com/maps/place/{latitude},{longitude}")
                    elif utilisation == 2:
                        try:
                            window = webview.create_window('GoogleMaps',f'https://www.google.com/maps/place/{latitude},{longitude}', width=1200, height=800)
                            print("Veuillez fermer la fenêtre pour continuer.")
                            webview.start()
                        except:
                            print("La page python n'a pas réussi à s'ouvrir", "\n", "Le page s'ouvre alors avec votre navigateur...")
                            webbrowser.open(f"https://www.google.com/maps/place/{latitude},{longitude}")
                print("Voulez-vous continuer vos recherches ? : ", "\n", "1 | Trouver une autre borne","\n", "2 | Trouver une autre ville","\n", "3 | Arrêter le programme",)
                choix = int(input("1/2/3 : "))
                while choix not in [1,2,3]:
                    choix = int(input("1/2/3 : "))
                else:
                    if choix == 1:
                        rep = int(input("Chiffre : "))-1
                        bonnombre = False
                    elif choix == 2:
                        bonnombre = True
                        main(utilisation)
                    elif choix == 3:
                        break
                    
            except:
                print("Vous avez choisi un nombre qui n'est pas dans la liste des bornes")
                rep = int(input("Chiffre : "))-1

    except:
        print("Il n'y a pas de bornes dans cette ville choissisez une autre ville")
        main(utilisation)


if __name__ == "__main__":
    print("\n","Préférez-vous ouvrir la page internet sur votre navigateur ou dans une fenêtre python ?","\n","1 | Navigateur","\n","2 | Python")
    utilisation = int(input("1/2 : "))
    while utilisation not in [1,2]:
        utilisation = int(input("1/2 : "))
    main(utilisation)
