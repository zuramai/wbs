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

      if(this.value == "cgroups") {
        $('#cgroups_only').css('display','block')
      }else{
        $('#cgroups_only').css('display','none')
      }
    });
    $('input[type=radio][name=sender]').change(function() {
      if (this.value == 'randomSender') {
          $('#randomSenderOnly').css('display','block')
          $('#chooseSenderOnly').css('display','none')
      } else if(this.value == 'chooseSender') {
          $('#randomSenderOnly').css('display','none')
          $('#chooseSenderOnly').css('display','block')
      }else{
          $('#randomSenderOnly').css('display','none')
          $('#chooseSenderOnly').css('display','none')
      }

    });

    $('.textarea').keyup(function(event) {
      var text = $(".textarea").val();   
      var lines = text.split(/\r|\r\n|\n/);
      var count = lines.length;
      $('.count').val(count)
      console.log(count)
    });

});