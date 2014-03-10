function handleFileSelect(event) {
  event.stopPropagation();
  event.preventDefault();

  var files = event.dataTransfer.files; // FileList object.

  // Loop through the FileList and render image files as thumbnails.
  for (var i = 0, file; file = files[i]; i++) {
    console.log(file.type);
    // Only process image files.
    if (!file.type.match('text/plain')) {
      continue;
    }
    var reader = new FileReader();
    var requirements = document.getElementById('id_requirements');
    // Closure to capture the file information.
    reader.onload = (function(theFile) {
      return function(e) {
        requirements.value = e.target.result;
        $('textarea').trigger('autosize.resize');
      };
    })(file);

    // Read in the image file as a data URL.
    reader.readAsText(file);
  }
}

function handleDragOver(event) {
  event.stopPropagation();
  event.preventDefault();
  event.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}

jQuery(document).ready(function ($) {
  var target = document.getElementById('spinner');
  var spinner = new Spinner({
    lines: 17, // The number of lines to draw
    length: 5, // The length of each line
    width: 6, // The line thickness
    radius: 30, // The radius of the inner circle
    corners: 0.7, // Corner roundness (0..1)
    rotate: 0, // The rotation offset
    direction: 1, // 1: clockwise, -1: counterclockwise
    color: '#000', // #rgb or #rrggbb or array of colors
    speed: 1, // Rounds per second
    trail: 52, // Afterglow percentage
    shadow: false, // Whether to render a shadow
    hwaccel: true, // Whether to use hardware acceleration
    className: 'spinner', // The CSS class to assign to the spinner
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    top: 'auto', // Top position relative to parent in px
    left: 'auto' // Left position relative to parent in px
  });
  spinner.spin(target);
  var tries = 600;
  var time = 3000;
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

  function finish() {
    spinner.stop();
    $.pjax({
      url: window.location,
      container: '#content',
      push: false
    })
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
        finish();
      }
    }).fail(function() {
      giveup();
    });
  }

  if (!$('#content').hasClass('finished')) {
    schedule();
  }

  $('textarea').autosize();

  $(document).on('keydown', 'textarea', function(e) {
    if(e.keyCode == 13 && (e.metaKey || e.ctrlKey)) {
      $(this).parents('form').submit();
    }
  });
});
