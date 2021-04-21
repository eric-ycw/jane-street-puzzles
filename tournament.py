import numpy as np
import itertools
import matplotlib.pyplot as plt

def win(p1, p2, players):
    # Returns the probaility that p1 wins against p2
    return players[p2] / (players[p1] + players[p2])

class TournamentTree:
    def __init__(self, players, win_prob):
        self.players = [float(p) for p in players]
        self.win_prob = win_prob

        self.init_players = players

    def fill_win_prob(self):

        # Fill the first column of win proabilities
        for i in range(0, len(self.players), 2):
            a, b = self.players[i], self.players[i+1]

            self.win_prob[i][0] = b/(a+b)
            self.win_prob[i+1][0] = a/(a+b)

        # Fill the first column of win proabilities
        for i in range(0, len(self.players), 4):
            a, b, c, d = self.players[i], self.players[i+1], \
                         self.players[i+2], self.players[i+3]

            self.win_prob[i][1] = self.win_prob[i][0] * (c*d)/(c+d) * (1/(a+c) + 1/(a+d))
            self.win_prob[i+1][1] = self.win_prob[i+1][0] * (c*d)/(c+d) * (1/(b+c) + 1/(b+d))
            self.win_prob[i+2][1] = self.win_prob[i+2][0] * (a*b)/(a+b) * (1/(c+a) + 1/(c+b))
            self.win_prob[i+3][1] = self.win_prob[i+3][0] * (a*b)/(a+b) * (1/(d+a) + 1/(d+b))

        # Fill the second column of win proabilities
        for i in range(0, len(self.players), 8):

            for j in range(4):
                self.win_prob[i+j][2] = self.win_prob[i+j][1] * ( \
                                            self.win_prob[i+4][1] * win(i+j, i+4, self.players) + \
                                            self.win_prob[i+5][1] * win(i+j, i+5, self.players) + \
                                            self.win_prob[i+6][1] * win(i+j, i+6, self.players) + \
                                            self.win_prob[i+7][1] * win(i+j, i+7, self.players) \
                                        )
            for j in range(4, 8):
                self.win_prob[i+j][2] = self.win_prob[i+j][1] * ( \
                                            self.win_prob[i][1] * win(i+j, i, self.players) + \
                                            self.win_prob[i+1][1] * win(i+j, i+1, self.players) + \
                                            self.win_prob[i+2][1] * win(i+j, i+2, self.players) + \
                                            self.win_prob[i+3][1] * win(i+j, i+3, self.players) \
                                        )

    def get_win_prob(self, player):
        pos = self.players.index(player)

        s = 0
        if pos < 8:
            for i in range(8, 16):
                s += self.win_prob[i][2] * win(pos, i, self.players)

        else:
            for i in range(8):
                s += self.win_prob[i][2] * win(pos, i, self.players)

        return self.win_prob[pos][2] * s

win_prob = np.zeros(shape=(16,3))

players = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]

tournament = TournamentTree(players, win_prob)
tournament.fill_win_prob()

# print(tournament.win_prob)
# print(np.sum(tournament.win_prob, axis=0))

base_win = tournament.get_win_prob(2)
print('\nBase winning probability:', base_win)

swaps = []
for i, j in itertools.combinations(range(16), 2):
    swap = players.copy()
    swap[i], swap[j] = swap[j], swap[i]
    swaps.append([swap, i, j])

best_win = base_win
best_swap = players


swaps_win_prob = []


for s in swaps:
    tournament = TournamentTree(s[0], np.zeros(shape=(16,3)))
    tournament.fill_win_prob()
    cur_win = tournament.get_win_prob(2)

    if cur_win > best_win:
        best_win = cur_win
        best_swap = s
    swaps_win_prob.append((str(players[s[1]]) + ' and ' + str(players[s[2]]), cur_win))

print('We should swap ' + str(players[best_swap[1]]) + ' and ' + str(players[best_swap[2]]))
print('Best winning probability for 2-seed:', best_win)
print('This leads to an increase in winning chances by', best_win - base_win)

plt.plot([i[0] for i in swaps_win_prob], [i[1] for i in swaps_win_prob])
plt.xticks(rotation=90, fontsize=6)
plt.axhline(y=base_win, color='r', linestyle='-')
plt.show()
