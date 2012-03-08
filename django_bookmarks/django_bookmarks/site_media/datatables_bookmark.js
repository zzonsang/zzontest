/* Global var for counter */
var giCount = 1;

 
$(document).ready(function() {
    $('#example').dataTable();
} );
 
function fnClickAddRow() {
	var item = $("#datatable")
    $('#example').dataTable().fnAddData( [
		item.find("#id_url").val(),
		item.find("#id_title").val(),
		item.find("#id_tags").val(),
        ]
    );
     
}