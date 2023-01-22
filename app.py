from flask import Flask, render_template, request, sessions,redirect
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1000
app.secret_key=os.getenv('secret')

from Rankings import Rankings
import fetch

# Main Page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# From Table
@app.route('/table/<string:name>', methods=['GET'])
def table(name):
        df = fetch.getTable(name)
        titles = {
            'sl': 'Satellite',
            'st': 'Stella',
            '★': 'Insane',
            '★★': 'Overjoy',
            '▼': 'Insane2',
            '双': 'Gachimijoy',
            '速い': 'Delay',
            'dl': 'ディレイjoy',
            'dpsl': 'DP Satellite',
            'δ': 'DP Delta',
            'h◎':'Scratch',
            '◆': 'LN'
            }
            
        if name == 'dpsl':
            name = 'sl'
            titles[name] = "DP Satellite"
        
        return render_template('table.html', PageTitle = titles[name], name = name, data=df, cols=df.columns, ignore=['LEVEL','CHART','TITLE','md5'])

# Search BMS
@app.route('/search', methods=['POST'])
def search():
        search = Rankings()
        search.createSearchDf(request.form['search'])
        return render_template('search.html', PageTitle = request.form['search'], data=search.df, cols=search.df.columns,ignore=['CHART','TITLE'])

# Get chart link
@app.route('/chart/<int:id>', methods=['GET'])
def chart(id):
    return redirect("http://www.ribbit.xyz/bms/score/view?md5={}".format(fetch.md5fromid(id)))

# File Upload
@app.route('/file', methods=['POST'])
def file():
    rankings = Rankings()
    rankings.createDf(fetch.md5fromfile(request.files['file']))
    return render_template('ranking.html', PageTitle = rankings.title, md5=fetch.md5fromfile(request.files['file']), table=[rankings.df.to_html(classes='table table-hover table-sm table-bordered', justify='left',index=False)], plot=rankings.plot)

# MD5
@app.route('/md5', methods=['POST'])
@app.route('/md5/<string:md5>', methods=['GET','POST'])
def md5(md5 = 0):
    rankings = Rankings()

    if md5 == 0:
        md5 = request.form['md5']

    rankings.createDf(md5)

    return render_template('ranking.html', PageTitle = rankings.title, md5=md5, table=[rankings.df.to_html(classes='table table-hover table-sm table-bordered',justify='left',index=False)], plot=rankings.plot)

# LR2IR ID
@app.route('/id', methods=['POST'])
@app.route('/id/<int:id>', methods=['GET','POST'])
def id(id = 0):
    rankings = Rankings()

    if id == 0:
        md5=fetch.md5fromid(request.form['id'])
    else:
        md5=fetch.md5fromid(id)

    rankings.createDf(md5)
    return render_template('ranking.html', PageTitle = rankings.title, md5=md5, table=[rankings.df.to_html(classes='table table-hover table-sm table-bordered',justify='left',index=False)], plot=rankings.plot)
    
# Errors
@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('index.html', error="BMS Not Found")

if __name__ == '__main__':
    app.run()