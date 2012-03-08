/* Global var for counter */
var giCount = 1;

 
$(document).ready(function() {
    $('#example').dataTable();
} );
 
function fnClickAddRow() {
	var item = $("#datatable")
    $('#example').dataTable().fnAddData( [
//		encodeURIComponent( item.find("#id_engine").val() ),
		item.find("#id_engine").val(),
		item.find("#id_browser").val(),
		item.find("#id_platform").val(),
		item.find("#id_version").val(),
		item.find("#id_grade").val()        
        ]
    );
     
}