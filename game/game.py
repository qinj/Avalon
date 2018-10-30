import random


class Board(object):
    def __init__(self, num_players):
        self.num_players = num_players
        self.board_players = self.create_board(num_players) # list
        self.mission_rounds = ['-','-','-','-','-'] #Success or Fail
        self.teams_per_mission_round = ['','','','','']
        self.vote_tracker = 0
    @staticmethod
    def create_board(num_players):
        board_dict = {5: [2, 3, 2, 3, 3],
                      6: [2, 3, 4, 3, 4],
                      7: [2, 3, 3, -4, 4],
                      8: [3, 4, 4, -5, 5],
                      9: [3, 4, 4, -5, 5],
                      10: [3, 3, 3, -5, 5]}
        return board_dict[num_players]

    def board_result(self, mission_round, team):
        self.teams_per_mission_round[mission_round] = team

    def __str__(self):
        return "Status of the game: " + ''.join(self.mission_rounds) + '\n' + \
               "Vote Tracker at: " + str(self.vote_tracker)

    def get_mission_rounds(self):
        return self.mission_rounds

    def set_mission_rounds(self, mission_round, result):
        assert type(mission_round) is int
        assert type(result) is str
        self.mission_rounds[mission_round] = result


class Player(object):
    def __init__(self, player_number, name, role):
        self.player_number = player_number
        self.name = name
        self.role = role
        self.votes = [False, False, False, False, False]  #T: accept F: reject
        self.leader = False

    def __str__(self):
        return "Player Number: " + str(self.player_number) + \
               " Name: " + self.name

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def set_accept_vote(self, mission_round):
        self.votes[mission_round] = True

    def get_vote(self):
        return self.votes

    def set_leader(self):
        self.leader = True

    def remove_leader(self):
        self.leader = False

    def is_leader(self):
        return self.leader


class Game(object):
    @staticmethod
    def get_evil_characters(num_players):
        bad_guys_dict = {5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4}
        return bad_guys_dict[num_players]

    @staticmethod
    def get_roles(num_players):
        roles_dict = {5: ['Merlin',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Minion of Mordred',
                          'Assassin'],
                      6: ['Merlin',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Minion of Mordred',
                          'Assassin'],
                      7: ['Merlin',
                          'Percival',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Minion of Mordred',
                          'Assassin',
                          'Morgana'],
                      8: ['Merlin',
                          'Percival',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Minion of Mordred',
                          'Assassin',
                          'Morgana'],
                      9: ['Merlin',
                          'Percival',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Loyal Servant of Arthur',
                          'Mordred',
                          'Assassin',
                          'Morgana'],
                      10: ['Merlin',
                           'Percival',
                           'Loyal Servant of Arthur',
                           'Loyal Servant of Arthur',
                           'Loyal Servant of Arthur',
                           'Loyal Servant of Arthur',
                           'Mordred',
                           'Assassin',
                           'Morgana',
                           'Oberon']}
        return roles_dict[num_players]
    @classmethod
    def create_players(cls, num_players):
        p = []
        player_names = []
        roles = cls.get_roles(num_players)
        rand_dict = {}
        for i in range(num_players):
            rand_num = random.randint(0, num_players-1)
            while True:
                if rand_num not in rand_dict.keys():
                    rand_dict[rand_num] = 1
                    break
                else:
                    rand_num = random.randint(0, num_players-1)
            name = input('Player ' + str(i + 1) + ' Enter your name: ')
            while name in player_names:
                name = input('Name already taken. Player ' + str(i + 1) + ' Enter your name: ')
            player_names.append(name)
            p.append(Player(i + 1, name, roles[rand_num]))
        return p

    @staticmethod
    def get_assassin(players):
        for player in players:
            if player.get_role() == 'Assassin':
                return player.name
        return "Assassin is not in the game."

    @staticmethod
    def pick_leader(num_players, players):
        while True:
            leader_random = input("Do you want to a random leader? (y/n) ")
            if leader_random == 'y':
                leader = random.randint(0, num_players - 1)
                return leader
            elif leader_random == 'n':
                for player in players:
                    print(player)
                leader = input("Pick a player number to set the leader. ")
                while not leader.isdigit():
                    leader = input("Not a number. Pick a player number to set the leader. ")
                while 0 > int(leader) > num_players:
                    leader = int(input("Player number does not exist. Pick a player number to set the leader. "))
                leader = int(leader)
                leader -= 1
                return leader
            print("Invalid input.")


    @staticmethod
    def create_team(board, players, leader, mission_round):
        while True:
            player_list = [player.get_name() for player in players]
            print(player_list)
            num_remaining = abs(board.board_players[mission_round])
            team = []
            players_on_team = []
            for i in range(num_remaining):
                member = input("Names must be in the list above. " +
                               str(num_remaining - i) + " more players go on this mission. ")
                while member not in player_list:
                    print("Current team: ", end="")
                    [print(member, end="") for member in players_on_team]
                    member = input("Player is not in the available players. Please select again. ")

                team.append(member)
                players_on_team.append(member)
            while True:
                print("\nTeam: ", end="")
                [print(member, end=" ") for member in team]
                confirm_team = input("\nIs this team correct? (Y/n) ")
                if confirm_team is 'Y':
                    return team
                elif confirm_team is 'n':
                    print("Please recreate your team. ")
                    break
                else:
                    print("Please choose 'Y' or 'n'. ")

    @staticmethod
    def cast_votes(players, mission_round):
        decision = False
        vote_list = []
        accept_votes = 0
        reject_votes = 0
        for player in players:
            while True:
                vote = input(player.get_name() + " place your vote. (y/n) ")
                if vote is 'y' or vote is 'n':
                    vote_list.append((player.get_name(), vote))
                    if vote is 'y':
                        player.set_accept_vote(mission_round)
                        accept_votes += 1
                    else:
                        reject_votes += 1
                    break
                else:
                    print("Please use y or n.")
                    continue
        print(vote_list)
        if accept_votes > reject_votes:
            print("\nMission is accepted by the council.\n")
            decision = True
        else:
            print("\nMission is rejected by the council.\n")

        return decision

    @staticmethod
    def go_on_mission(team, two_fails_required):
        result = False
        pass_results = 0
        fail_results = 0
        for member in team:
            while True:
                member_result = input(member + " what is the result? (pass/fail) ")
                if member_result == 'pass':
                    pass_results += 1
                    break
                elif member_result == 'fail':
                    fail_results += 1
                    break
                print("That is not an option.")
                continue

        if fail_results < 1:
            result = True
        else:
            if two_fails_required and fail_results < 2:
                result = True
        return result

    def play(self):
        num_success = 0
        num_fail = 0
        mission_round = 0
        while True:
            num_players = input('How many players are there? ')
            if num_players.isdigit():
                if 5 > int(num_players) < 10:
                    print("Not a number between 5 and 10. Try again")
                    continue
            else:
                print("Not a number between 5 and 10. Try again")
                continue
            break
        num_players = int(num_players)
        board = Board(num_players)

        # create players
        players = self.create_players(num_players)
        leader = self.pick_leader(num_players=num_players, players=players)
        # game start
        while num_success < 3 and num_fail < 3:
            two_fails_required = False
            if board.board_players[mission_round] < 0:
                two_fails_required = True
            print(players[leader].get_name() + " is the leader. Pick your team.")

            # selecting team
            team = self.create_team(board, players, leader, mission_round)
            print("\nTeam: ", end="")
            [print(member, end=" ") for member in team]
            print("\nTime to vote.\n")
            # vote
            decision = self.cast_votes(players=players, mission_round=mission_round)
            # go on mission or not
            if decision:
                result = self.go_on_mission(team=team, two_fails_required=two_fails_required)
                if result:
                    num_success += 1
                    print("\nMission " + str(mission_round + 1) + " is a success.\n")
                else:
                    num_fail += 1
                    print("\nMission " + str(mission_round + 1) + " is a fail.\n")
                mission_round += 1
            print("\nNew leader.\n")
            players[leader].remove_leader()
            leader += 1
            leader %= num_players
            players[leader].set_leader()
        # Assassin
        if num_success >= 3:
            assassin = self.get_assassin(players)
            print('\n\n____________Will erase after game is built____________')
            for player in players:
                print(player.get_role())
            print('______________________________________________________\n\n')
            for player in players:
                print(player)
            answer = input(assassin + " is the Assassin. Find Merlin. (Enter player number). ")
            if players[int(answer)-1].get_role() == 'Merlin':
                print("Assassin found Merlin. Mordred wins.")
            else:
                print("Merlin wins.")
        else:
            print("Mordred wins.")
        print("Thanks for playing Avalon!")


playGame = Game()
playGame.play()