import pandas as pd
from NBA import app
from flask import render_template, request
import nba_api.stats.endpoints
#from nba_api.stats.static import teams


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    team1 = request.form['team1']
    team2 = request.form['team2']

    team1_data = nba_api.stats.endpoints.LeagueDashTeamShotLocations(team_id_nullable=team1,per_mode_detailed="PerGame").get_data_frames()[0]
    team2_data = nba_api.stats.endpoints.LeagueDashTeamShotLocations(team_id_nullable=team2,per_mode_detailed="PerGame").get_data_frames()[0]

    # 表作成
    comparison = pd.concat([team1_data, team2_data], axis=0, keys=[team1, team2])
    # 不要な列を削除
    comparison = comparison.drop(comparison.columns[[0, 11, 12, 13, 14, 15, 16, 20, 21, 22]], axis=1)
    # 数字だけで差を計算
    difference = comparison.select_dtypes(include='number').diff(periods=-1).dropna()
    # 差を追加
    comparison = comparison.append(difference, ignore_index=True)
    # 追加した行のインデックスを取得
    index = comparison.index[-1]
    # columns[1]の値をcomparisonに変更
    comparison.loc[index, comparison.columns[0]] = 'comparison'

    comparison_html = comparison.to_html(classes='table table-striped', border=1, justify='center', decimal=',')

    return render_template('comparison.html', comparison=comparison_html)

if __name__ == '__main__':
    app.run(debug=True)