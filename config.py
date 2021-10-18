token = 'a13720c4d07377141b453a1f43ff9b2c7c7f10cc55d5a419552ec5bddd380771444a101f64aaeda1ae921'

import requests
from bs4 import BeautifulSoup
from pprint import pprint

class Parser:

    '''
    plancke.io parsing for bedwars and sw statistic
    '''

    def __init__(self):

        self.available_modes = ["bw", "sw"]
        self.available_umodes = {"bw": ["solo", "doubles"], "sw": ["normal", "insane"]}

        self.modes = {"bw":'collapse-1-2', "sw": "collapse-1-9"}
        self.modes_header = {"bw":  [3, 1], "sw": [0, 3]}
        self.umodes_table_sw = {"insane": 1, "normal": 0}
        self.umodes_table_bw = {"solo": [0], "doubles": [1]}
        self.header_template = "Stats | {mode} {umode}{bw_doubles} | {name}\nLevel: {level}\nCoins: {coins}\n\n"
        self.return_template_sw = "Kills: {}\nDeathes: {}\n\nWins: {}\nLoses: {}"
        self.return_template_bw = "Normal Kills: {}\nFinal Kills: {}\nNormal Deathes: {}\nFinal Deathes: {}\n\nWins: {}\nLoses: {}\nBeds Broken: {}"


    def parsePlanckeIO(self, mode, umode, name):
        
        req = requests.get(f'https://plancke.io/hypixel/player/stats/{name}')

        if req.status_code != 200:
            return ''

        soup = BeautifulSoup(req.text, 'html.parser')

        mode_content = soup.find(id=self.modes[mode])

        ## data collecting part
        # header part (lvl + coins)
        header = mode_content.ul.contents  
        lvl = header[self.modes_header[mode][0]].contents[1]
        lvl = lvl.replace(' ', '')
        coins = header[self.modes_header[mode][1]].contents[1]
        coins = coins.replace(' ', '')

        if umode == "doubles":
            msg_header = self.header_template.format(mode=mode, umode=umode, name=name, level=lvl, coins=coins, bw_doubles="👨‍❤‍👨")
        else:
            msg_header = self.header_template.format(mode=mode, umode=umode, name=name, level=lvl, coins=coins, bw_doubles="")
        # end part

        
        if mode == "bw":
            table_rows = mode_content.table.contents[3:]
            
            row = table_rows[self.umodes_table_bw[umode][0]]
            intel = row.contents[1:]

            normal_kills = intel[0].contents[0]
            final_kills = intel[3].contents[0]

            n_deathes = intel[1].contents[0]
            f_deathes = intel[4].contents[0]

            wins = intel[6].contents[0]
            loses = intel[7].contents[0]
            beds = intel[-1].contents[0]
            
            msg_body = self.return_template_bw.format(normal_kills, final_kills, n_deathes, f_deathes, wins, loses, beds)

        elif mode == "sw":
            table_rows = mode_content.table.contents[2:]
            row = table_rows[self.umodes_table_sw[umode]].contents
            
            kills = row[1].contents[0]
            deathes = row[2].contents[0]

            wins = row[-3].contents[0]
            loses = row[-2].contents[0]

            msg_body = self.return_template_sw.format(kills, deathes, wins, loses)

        
        return msg_header + msg_body

