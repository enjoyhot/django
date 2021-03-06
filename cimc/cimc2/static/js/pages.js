function setPage(object,num){
	var contents=
	"<ul class=\"pagination\">\
{% if "+object+".has_previous %}\
    <li><a href=\"?table=1&&page={{ "+object+".previous_page_number }}\" class=\"prev\">{{ previous_link_decorator|safe }}上一页</a></li>\
{% else %}\
    <li class=\"paginate_button previous disabled\"><span class=\"disabled prev\">{{ previous_link_decorator|safe }}上一页</span></li>\
{% endif %}\
{% for page in "+object+".paginator.page_range %}\
{% if page %}\
{% ifequal page "+object+".number %}\
<li class=\"active\"><span class=\"current page\">{{ page }}</span></li>\
{% else %}\
<li><a href=\"?table=1&&page{{ page_suffix }}={{ page }}{{ getvars }}\" class=\"page\">{{ page }}</a></li>\
{% endifequal %}\
{% else %}\
      <li>...</li>\
{% endif %}\
{% endfor %}\
{% if "+object+".has_next %}\
        <li><a href=\"?table=1&&page={{ "+object+".next_page_number }}\" class=\"next\">下一页{{ next_link_decorator|safe }}</a></li>\
{% else %}\
        <li class=\"paginate_button next disabled\"><span class=\"disabled next\">下一页{{ next_link_decorator|safe }}</span></li>\
{% endif %}\
</ul>\
";
	$('#pages').html(contents);
}