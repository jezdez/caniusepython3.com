jQuery(document).ready(function ($) {
  var target = document.getElementById('spinner');
  var spinner = new Spinner({
    lines: 17, // The number of lines to draw
    length: 5, // The length of each line
    width: 2, // The line thickness
    radius: 10, // The radius of the inner circle
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

  $('#shield-code').focus(function() {
      var $this = $(this);
      $this.select();

      // Work around Chrome's little problem
      $this.mouseup(function() {
          // Prevent further mouseup intervention
          $this.unbind('mouseup');
          return false;
      });
  });

  // define some default snippets for the shields
  var shields = {
    'image': '{{shield}}',
    'restructuredtext': '.. image:: {{shield}}\n    :target: {{home}}',
    'markdown': '[![Can I Use Python 3?]({{shield}})]({{home}})',
    'textile': '!{{shield}}!:{{home}}',
    'rdoc': '{<img src="{{shield}}" alt="Can I Use Python 3?" />}[{{home}}]',
    'asciidoc': 'image:{{shield}}["Can I Use Python 3?", link="{{home}}"]',
  }
  var render_shield = function(select) {
    var template = shields[select.val()];
    if (template) {
      // populate a rendering context
      var context = {
        'shield': select.data('shield'),
        'home': select.data('home'),
      }
      var output = Mustache.render(template, context);
      $('#shield-code').html(output).autosize().trigger('autosize.resize');
    };
  };
  $(document).on('change', '#shield-select', function(event) {
    event.preventDefault();
    render_shield($(this));
  }).find("#shield-select option:selected").each(function() {
    render_shield($(this).parent());
  });
});
