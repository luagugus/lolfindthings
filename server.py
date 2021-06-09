
from riotwatcher import LolWatcher, ApiError
import pandas as pd
from flask import Flask, render_template, request

# golbal variables
api_key = 'Your api key'
watcher = LolWatcher(api_key)
my_region = 'kr'

app = Flask(__name__)


@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    return render_template('mains.html')

@app.route('/post', methods=['POST'])
def post():
    try:
        value = request.form['username']
        me = watcher.summoner.by_name(my_region, value)
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
        icon1 = "http://ddragon.leagueoflegends.com/cdn/11.10.1/img/profileicon/"+str(me["profileIconId"])+".png"    

        t = me['name']
        c = me['summonerLevel']
        my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])
    
        last_match = my_matches['matches'][0]
        print(my_matches['matches'])
        match_detail = watcher.match.by_id(my_region, last_match['gameId'])
        participants = ["","","","","","","","","",""]
        us = match_detail['participantIdentities']
    except:
        return "검색오류. 서버에 그이름을 가진 유저가 없습니다."

    index = -1

    for row in match_detail['participants']: 
        
        participants_row = {}
        index = index + 1
        uo = us[index]['player']
        participants_row['이름'] = uo['summonerName']
        participants_row['승패'] = row['stats']['win']
        participants_row['킬'] = row['stats']['kills']
        participants_row['데스'] = row['stats']['deaths']
        participants_row['어시'] = row['stats']['assists']
        participants_row['챔프렙'] = row['stats']['champLevel']

        participants[index] = participants_row


    try:
        win = my_ranked_stats[0]['wins']
        losse = my_ranked_stats[0]['losses']
        uid = win + losse
        end = win / uid * 100

            
        return render_template('realit.html', name = t, level = c, win = round(end),icon = icon1, game = participants)
    except:
        td = "--"
        return render_template('realit.html', name = t, level = c, win = td,icon = icon1, game = participants)

@app.route('/jumjuk', methods=['POST'])
def jun():
    value = request.form['username']
    value1 = request.form['int']
    me = watcher.summoner.by_name(my_region, value)
    my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    icon1 = "http://ddragon.leagueoflegends.com/cdn/11.10.1/img/profileicon/"+str(me["profileIconId"])+".png"    

    t = me['name']
    my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])
    
    last_match = my_matches['matches'][int(value1)]
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])
    participants = ["","","","","","","","","",""]
    us = match_detail['participantIdentities']

    index = -1

    for row in match_detail['participants']: 
        
        participants_row = {}
        index = index + 1
        uo = us[index]['player']
        participants_row['이름'] = uo['summonerName']#name
        participants_row['승패'] = row['stats']['win']#wind or lose to bool
        participants_row['킬'] = row['stats']['kills']#kill
        participants_row['데스'] = row['stats']['deaths']#dead
        participants_row['어시'] = row['stats']['assists']#what? supportkill?
        participants_row['챔프렙'] = row['stats']['champLevel']# level(chamions)

        participants[index] = participants_row
    print(participants[1])

    return render_template('realit2.html', name = t,icon = icon1, game = participants)


    
    



if __name__ == '__main__':
    app.run(debug=True)
