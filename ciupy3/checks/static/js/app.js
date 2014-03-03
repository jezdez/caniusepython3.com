jQuery(document).ready(function ($) {
  var tries = 60;
  var time = 2000;
  checked = 0;

  function giveup() {
    $('.wait-message').hide();
    $('.error-message').show();
  }

  function schedule() {
    if (checked < tries) {
      setTimeout(function(){check()}, time);
    } else {
      giveup();
    }
  }

  function check() {
    $.ajax({
      cache: false,
      dataType: 'json',
      url: window.location
    }).done(function(data) {
      checked++;
      if (data.finished_at == null) {
        schedule();
      } else {
        $.pjax({
          url: window.location,
          container: '#content',
          push: false
        })
      }
    }).fail(function() {
      giveup();
    });
  }

  if (!$('#content').hasClass('finished')) {
    schedule();
  }
});
