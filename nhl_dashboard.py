import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------
# Models
# -----------------------------
class Player:
    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position
        self.stats = {}  # Placeholder for stats like goals, assists, etc.

class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.stats = {}   # Placeholder for team stats
        self.roster = []  # List of Player objects

# -----------------------------
# API Handler
# -----------------------------
class NHLApi:
    def get_teams(self):
        # Placeholder: return a list of Team objects
        return [
            Team(1, "Boston Bruins"),
            Team(2, "Toronto Maple Leafs"),
            Team(3, "Chicago Blackhawks")
        ]

    def get_team_roster(self, team_id):
        # Placeholder: return a list of Player objects
        return [
            Player(101, "Player A", "Forward"),
            Player(102, "Player B", "Defense"),
            Player(103, "Player C", "Goalie")
        ]

    def get_player_stats(self, player_id):
        # Placeholder: return dictionary of player stats
        return {
            "Games Played": 82,
            "Goals": 25,
            "Assists": 40,
            "Points": 65
        }

# -----------------------------
# GUI Application
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("NHL Team and Player Stats")
        self.root.geometry("600x400")

        self.api = NHLApi()
        self.teams = self.api.get_teams()
        self.selected_team = None
        self.selected_player = None

        self.create_widgets()

    def create_widgets(self):
        # --- Team selector ---
        tk.Label(self.root, text="Select Team:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        team_names = [team.name for team in self.teams]
        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(self.root, textvariable=self.team_var, values=team_names, state="readonly")
        self.team_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.team_dropdown.bind("<<ComboboxSelected>>", self.on_team_selected)

        # --- Roster listbox ---
        tk.Label(self.root, text="Roster:").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.roster_listbox = tk.Listbox(self.root, height=10)
        self.roster_listbox.grid(row=1, column=1, padx=10, pady=10, sticky="n")
        self.roster_listbox.bind("<<ListboxSelect>>", self.on_player_selected)

        # --- Player stats display ---
        tk.Label(self.root, text="Player Stats:").grid(row=1, column=2, padx=10, pady=10, sticky="nw")
        self.stats_text = tk.Text(self.root, width=30, height=10, state="disabled")
        self.stats_text.grid(row=1, column=3, padx=10, pady=10, sticky="n")

    # --- Event Handlers ---
    def on_team_selected(self, event):
        selected_name = self.team_var.get()
        self.selected_team = next((team for team in self.teams if team.name == selected_name), None)
        if self.selected_team:
            self.selected_team.roster = self.api.get_team_roster(self.selected_team.id)
            self.populate_roster_listbox()

    def populate_roster_listbox(self):
        self.roster_listbox.delete(0, tk.END)
        for player in self.selected_team.roster:
            self.roster_listbox.insert(tk.END, player.name)

    def on_player_selected(self, event):
        selection = self.roster_listbox.curselection()
        if not selection or not self.selected_team:
            return
        index = selection[0]
        self.selected_player = self.selected_team.roster[index]
        self.selected_player.stats = self.api.get_player_stats(self.selected_player.id)
        self.display_player_stats()

    def display_player_stats(self):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        if self.selected_player:
            for key, value in self.selected_player.stats.items():
                self.stats_text.insert(tk.END, f"{key}: {value}\n")
        self.stats_text.config(state="disabled")


# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
