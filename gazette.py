# -*- coding: utf-8 -*-

#import uniout
import sys
import json
import httplib2
from lxml import etree

MAX_PAGE = 310
GAZ_URL = "http://www.president.gov.tw/Default.aspx?tabid=84&Size=30&Page={page}&ctid=-1&sort=0&order=1"
base_url = "http://www.president.gov.tw"

def get_gaz(page=1):
    h = httplib2.Http(".cache")
    resp, cont = h.request(GAZ_URL.format(page=page),
                           headers={'cache-control': 'min-fresh=%s' % -(sys.maxsize >> 1)})
    
    root = etree.HTML(cont.decode('utf-8'))
    v = root.xpath("id('dnn_ctr428_LoadCtl_ctl00_GridView1')/tr/td")
    
    result = []
    print(len(v) == 150, len(v))
    if page == 264 or page == 265:
        return []
    
    for i in range(0, len(v), 5):
        data = {}
        data['publish_date'] = v[i + 1].text.strip("\r\n ")
        data['issue'] = v[i + 2].text.strip("\r\n ")
        data['title'] = v[i + 3].xpath("a")[0].values()[1]
        
        try:
            data['link'] = base_url + v[i + 3].xpath("a")[0].values()[2]
        except:
            data['link'] = "None"
        
        for i in v[i + 4].xpath("a"):
            if i.values()[-1].endswith("pdf"):
                data['link_pdf'] = base_url + i.values()[-1]
            elif i.values()[-1].endswith("doc"):
                data['link_doc'] = base_url + i.values()[-1]
        
        if "link_pdf" not in data: data['link_pdf'] = ""
        if "link_doc" not in data: data['link_doc'] = ""
        
        result.append(data)
        
    return result


def init_json(path):
    results = []
    for i in range(MAX_PAGE + 1):
        print(i)
        for j in get_gaz(i):
            results.append(j)
            
    open(path, "w").write(to_json(results))


def to_json(d):
    return json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4)


if __name__ == '__main__':
    env = os.environ.copy()
    env['GIT_DIR'] = env['PRESIDENT_OUTPUT_DIR']
    
    # to json
    os.chdir(env['PRESIDENT_OUTPUT_DIR'])
    if version_3k:
    	pass
        # update_schedules('president.json', 'president.json')
    else:
        print("Please use 3k...")
        exit()