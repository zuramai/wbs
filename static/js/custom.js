    // Use Morris.Area instead of Morris.Line
    
$(window).scroll(function() {
  var height = $(window).height();
  $('.sidebar').css('height',height);
})

$(document).ready(function() {
  $('#upload_csv').click(function() {
    $('#upload-csv').trigger('click')
  })

  $('#upload-csv').change(function() {
    $('#upload-file').submit();
  });
});