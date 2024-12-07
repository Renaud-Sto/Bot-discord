import discord
from discord.ext import commands

# Intents et configuration du bot
# Configuration des intents
intents = discord.Intents.default()
intents.messages = True  # Permet de lire le contenu des messages
intents.message_content = True  # Intents privilégiés pour le contenu des messages
bot = commands.Bot(command_prefix="!", intents=intents)

# ID du canal cible
TARGET_CHANNEL_ID = 1315004557729726586  # Remplacez par l'ID correct

# Dictionnaire pour stocker les données des sections
sections = {}

# Liste des métiers autorisés
ALLOWED_JOBS = ["Forgeron", "Forgemage", "Tailleur", "Costumage", "Cordonnier", "Cordomage", "Bijoutier", "Joaillomage", "Sculpteur", "Sculptemage",
                 "Façonneur", "Façomage", "Alchimiste", "Bricoleur", "Bûcheron", "Paysan", "Mineur", "pêcheur", "Chasseur"]

# Stocker le message initial pour le mettre à jour
initial_message = None

# Fonction pour construire le message formaté
def build_message_content():
    """Construit le contenu formaté des sections pour l'affichage."""
    global sections
    message = "Mettez à jour vos métiers avec la commande : `!update [nom] [métier] [niveau]`\n\n"
    for job, users in sections.items():
        message += f"== {job} ==\n"
        for name, level in users.items():
            message += f"- {name} : {level}\n"
        message += "\n"
    return message.strip()

@bot.event
async def on_ready():
    """Action lors de la connexion du bot."""
    print(f"Connecté en tant que {bot.user} !")
    global initial_message

    # Obtenir le canal cible
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not target_channel:
        print("Le canal cible est introuvable. Vérifiez l'ID.")
        return

    # Envoyer le message initial si ce n'est pas encore fait
    try:
        initial_content = build_message_content()
        initial_message = await target_channel.send(initial_content)
        print("Message initial envoyé.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du message initial : {e}")

@bot.command()
async def update(ctx, name: str, job: str, level: int):
    """Met à jour ou ajoute un utilisateur à une section."""
    global sections
    global initial_message

    # Vérifier si la commande est exécutée dans le bon canal
    if ctx.channel.id != TARGET_CHANNEL_ID:
        print(f"Commande reçue dans le mauvais canal : {ctx.channel.id}")
        await ctx.send(f"Cette commande ne peut être utilisée que dans <#{TARGET_CHANNEL_ID}>.")
        return

    # Normaliser le métier
    job = job.capitalize()

    # Vérifier si le métier est dans la liste des métiers autorisés
    if job not in ALLOWED_JOBS:
        try:
            await ctx.author.send(f"Le métier `{job}` n'est pas autorisé. Voici les métiers disponibles : {', '.join(ALLOWED_JOBS)}.")
        except discord.Forbidden:
            await ctx.send("Je ne peux pas vous envoyer de message privé. Veuillez vérifier vos paramètres de confidentialité.")
        await ctx.message.delete()  # Supprime le message de la commande
        return        

    # Ajouter ou mettre à jour les données
    if job not in sections:
        sections[job] = {}

    if name in sections[job]:
        sections[job][name] = level
        action = "mis à jour"
    else:
        sections[job][name] = level
        action = "ajouté"

    # Mettre à jour le message initial
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not target_channel:
        print("Canal cible introuvable lors de la mise à jour.")
        await ctx.send("Le canal cible est introuvable. Vérifiez l'ID dans le code.")
        return

    try:
        # Construire le nouveau contenu
        message_content = build_message_content()

        # Mettre à jour le message initial si possible
        if initial_message:
            print("Mise à jour du message initial.")
            await initial_message.edit(content=message_content)
        else:
            print("Réinitialisation du message initial.")
            initial_message = await target_channel.send(message_content)

        # # Informer l'utilisateur du succès
        # await ctx.send(f"{name} a été {action} dans la section {job} avec le niveau {level}.")

        # Supprimer le message de l'utilisateur
        await ctx.message.delete()  # Supprime le message de la commande
    except Exception as e:
        print(f"Erreur lors de la mise à jour du message initial : {e}")
        await ctx.send("Une erreur est survenue lors de la mise à jour.")

# Lancer le bot avec votre token
bot.run("MTMxNDk3MzUxOTkzODg0NjgwMQ.G-b3z8.D6P-t5DnU72Md9emsnFKKSUCDw-G_SqwKHqwpU")
