jQuery(document).ready(function ($) {
  var tries = 600;
  var time = 3000;
  checked = 0;

  function giveup() {
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

  $(document).on('pjax:complete', function() {
    $('textarea').autosize();
  })

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
    'image': '{{url}}.{{format}}',
    'html': '<a href="{{url}}" rel="nofollow" title="Can I Use Python 3?"><img src="{{url}}.{{format}}" alt="Can I Use Python 3?" /></a>',
    'restructuredtext': '.. image:: {{url}}.{{format}}\n    :target: {{url}}',
    'markdown': '[![Can I Use Python 3?]({{url}}.{{format}})]({{url}})',
    'textile': '!{{url}}.{{format}}!:{{url}}',
    'rdoc': '{<img src="{{url}}.{{format}}" alt="Can I Use Python 3?" />}[{{url}}]',
    'asciidoc': 'image:{{url}}.{{format}}["Can I Use Python 3?", link="{{url}}"]',
  }
  var render_shield = function(select) {
    var template = shields[select.val()];
    if (template) {
      if ($('#shield-format').prop('checked')) {
        var format = 'png';
      } else {
        var format = 'svg';
      };
      if ($('#shield-style').prop('checked')) {
        var format = format + '?style=flat';
      };
      var url = select.data('url');
      // populate a rendering context
      var context = {'url': url, 'format': format}
      $('#shield-example').attr('src', url + '.' + format);
      var output = Mustache.render(template, context);
      $('#shield-code').html(output).autosize().trigger('autosize.resize');
    };
  };
  $('#shield-select,#shield-format,#shield-style').on('change', function(event) {
    event.preventDefault();
    render_shield($('#shield-select'));
  })
  $("#shield-select option:selected").each(function() {
    render_shield($(this).parent());
  });

  $('#check-form').on('submit', function() {
    $('#check-submit').addClass('disabled').text('Checking..');
  });
});
