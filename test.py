import re
import sys
from subprocess import call
from bottle import Bottle, post, request

app = Bottle(__name__)

@app.route('/cin/<cin>')
def cin(cin):

	cin_id = cin

	call('curl https://www.zaubacorp.com/companysearchresults/'+cin_id+' > first.html',shell=True)

	fo = open("first.html","r+")
	data = fo.read(51200)
	res = re.findall(r'<td><a(.*?)>',data,re.DOTALL)
	res_url = res[0].split('"')
	final_cin_url = res_url[3]
	fo.close()

	call('curl '+final_cin_url+' > second.html',shell=True)

	fo = open("second.html","r+")
	data = fo.read(51200)
	res = re.findall(r'<table class="table table-striped col-md-12 col-sm-12 col-xs-12">(.*?)</table>',data,re.DOTALL)
	res_val = res[0].split('<tr>')

	cmp_name = res_val[2].split('<td>')
	cmp_name = cmp_name[2].split('<p>')
	cmp_name = cmp_name[1].split('</p>')

	reg_no = res_val[4].split('<td>')
	reg_no = reg_no[2].split('<p>')
	reg_no = reg_no[1].split('</p>')

	ac = res_val[9].split('<td>')
	ac = ac[2].split('<p>')
	ac = ac[1].split('</p>')

	print "Company Name : ",cmp_name[0]
	print "Reg No. : ",reg_no[0]
	print "Avg. Capital : ",ac[0]

	fo.close()
	return "{\"cin_status\":{\"Company Name\":\""+cmp_name[0]+"\",\"Registration No.\":\""+reg_no[0]+"\",\"Avg. Capital\":\""+ac[0]+"\" }}"