#coding:utf-8
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

'''
参数1：每页显示的条数
参数2：待显示数据列表
参数3：翻页时对应的表单
参数4：共处理表的数目
参数5：翻页时对应表对应的页码

前两个参数设置所有表
后三个参数只对应鼠标点击相应的表
'''
def get_page_msg(limit,selectItemList,index,count,page):
	
	p_pages = []
	resultItem = []
	for i in range(count):
		selectItemList[i]=Paginator(selectItemList[i],limit)

		p_pages.append(selectItemList[i].page_range[0:7])
		resultItem.append(selectItemList[i].page(1))

	if int(page) < 4:   #这里进行判断，假如当前页小于5的时候，
	        p_pages[index] = selectItemList[index].page_range[0:7]    #pr为获取页码列表，即当前页小于4的时候，模板中将显示第1页至第7页，如 1 2 3 4 5 6 7
	elif int(selectItemList[index].num_pages)-int(page) < 4:   #假如最后页减当前页小于4时
		num_pages=int(selectItemList[index].num_pages)
	        p_pages[index] = selectItemList[index].page_range[num_pages-7:num_pages]  #页码列表显示最后7页，如共有30页的话，那显示：24 25 26 27 28 29 30
	else:   #其它情况
	        p_pages[index] = selectItemList[index].page_range[int(page)-4:int(page)+3]   #其它情况显示当前页的前3条至后3条，如当前在第10页的话，那显示： 7 8 9 10 11 12 13 
	try:
		resultItem[index] = selectItemList[index].page(page)
	except EmptyPage:
		resultItem[index] = selectItemList[index].page(selectItemList[index].num_pages)
	return resultItem,p_pages
