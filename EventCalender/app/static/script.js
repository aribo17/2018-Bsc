$(document).ready(function(){
    $('#datatable1').DataTable();
});

$(document).ready(function(){
    $('#datatable2').DataTable({
        "scrollX": true
    });
});

$(document).ready(function(){
    $('#datatable3').DataTable({
        "scrollX": true
    });
});


$(document).ready(function(){
  $('.carousel-showmanymoveone .item').each(function(){
    var itemToClone = $(this);

    for (var i=1;i<6;i++) {
      itemToClone = itemToClone.next();

      // wrap around if at end of item collection
      if (!itemToClone.length) {
        itemToClone = $(this).siblings(':first');
      }

      // grab item, clone, add marker class, add to collection
      itemToClone.children(':first-child').clone()
        .addClass("cloneditem-"+(i))
        .appendTo($(this));
    }
  });
 });
