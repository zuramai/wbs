    // Use Morris.Area instead of Morris.Line
    
$(window).scroll(function() {
  var height = $('body').height();
  $('.sidebar').css('height',height);
})

$(document).ready(function() {
  $('#upload_csv').click(function() {
    $('#upload-csv').trigger('click')
  });

  Waves.attach('.waves-effect', ['waves-button', 'waves-circle'])
  Waves.init()

  $('#upload-csv').change(function() {
    $('#upload-file').trigger('click');
  });

    $('.datatable').DataTable();

    $('input[type=radio][name=type]').change(function() {
    if (this.value == 'single') {
        $('#single-only').css('display','block')
    } else {
        $('#single-only').css('display','none')
    }
});

});