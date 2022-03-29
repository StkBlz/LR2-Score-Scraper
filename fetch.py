import re
import requests
import hashlib
import pandas as pd

def md5fromid(id):
    id = re.search("(\d+)$",str(id))
    md5 = requests.get("http://www.ribbit.xyz/bms/search/run?search[value]={}".format(id.group(1)))
    try:
        return md5.json()['data'][0][0]
    except IndexError:
        raise Exception("BMS not found")

def md5fromfile(filename):
    file = filename.read()
    return hashlib.md5(file).hexdigest()

def getTable(name):
    url = {
        'sl':'https://stellabms.xyz/sl/score.json',
        'st':'https://stellabms.xyz/st/score.json',
        '★':'http://www.ribbit.xyz/bms/tables/insane_body.json',
        '★★':'http://www.ribbit.xyz/bms/tables/overjoy_body.json',
        'dpsl':'https://stellabms.xyz/dp/score.json',
        'δ':'http://dpbmsdelta.web.fc2.com/table/data/dpdelta_data.json'   ,
        '双':'https://script.googleusercontent.com/macros/echo?user_content_key=atyW8-CTQqlAdgJoDi0x-XMYHyin2iKMLhOC0_BgsB1MP2WVReHzg4ALxpCTcy31_iuAKPPo5i2ALSy0fU6prsvETDDOugOYm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnILVNktUN8QD5O8HG3VQM5Y0cDcGmbB7z-CdYfSApNPioZOcABHyMfp6Z51J_ZQagetfRKoxihmn&lib=Mo1-yJSaFFNepveXLq6oyILrR_qwrjn-o',  
        '速い':'https://kamikaze12345.github.io/github.io/delaytrainingtable/data.json',
        'dl':'https://script.googleusercontent.com/macros/echo?user_content_key=ejwinCiZIirJYGx5PCEgFCAayEOBcErooKcb5cL6PNUMAbChaHkNXY1pdbO185tunJIksjTWd_bKNP6Lt0B09nEH8DEm8rgam5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnMWvYyJ1GKyTMvfes66B8rrYejgxcMvakG9VGXk4ouLbL71REbiUG9pC5KitOC4regjXMfvf15DiLHQ20cXOO6tO69V4cxiB6g&lib=MfZa1yLnUJ2hsW8x-6kP3UZXvWRuAoVU2',
        '▼':'https://rattoto10.github.io/second_table/insane_data.json',
        'h◎':'http://minddnim.web.fc2.com/sara/3rd_hard/json/data.json',
        '◆':'http://flowermaster.web.fc2.com/lrnanido/gla/score.json'  
        }

    df = pd.read_json(url[name])
    df["CHART"] = None
    df = df[['level', 'title', 'CHART', 'artist', 'md5']]
    df.rename(columns={'level':'LEVEL', 'title':'TITLE','artist':'ARTIST'},inplace=True)
    return df