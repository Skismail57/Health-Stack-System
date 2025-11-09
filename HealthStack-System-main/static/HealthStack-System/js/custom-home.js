// Custom homepage animations and click-to-filter
(function($){
  $(function(){
    var $spec = $('.specialities-slider');
    if ($spec.length) {
      if ($spec.hasClass('slick-initialized')) { $spec.slick('unslick'); }
      $spec.slick({
        dots: true,
        autoplay: true,
        autoplaySpeed: 1000,
        speed: 800,
        infinite: true,
        variableWidth: true,
        prevArrow: false,
        nextArrow: false,
        pauseOnHover: false,
        pauseOnFocus: false,
        cssEase: 'ease-in-out'
      });
    }

    var $doc = $('.doctor-slider');
    if ($doc.length) {
      if ($doc.hasClass('slick-initialized')) { $doc.slick('unslick'); }
      $doc.slick({
        dots: false,
        autoplay: true,
        autoplaySpeed: 1000,
        speed: 800,
        infinite: true,
        variableWidth: true,
        pauseOnHover: false,
        pauseOnFocus: false,
        cssEase: 'ease-in-out'
      });
    }

    var $feat = $('.features-slider');
    if ($feat.length) {
      if ($feat.hasClass('slick-initialized')) { $feat.slick('unslick'); }
      $feat.slick({
        dots: true,
        infinite: true,
        centerMode: true,
        slidesToShow: 3,
        speed: 800,
        variableWidth: true,
        arrows: false,
        autoplay: true,
        autoplaySpeed: 1000,
        pauseOnHover: false,
        pauseOnFocus: false,
        responsive: [{ breakpoint: 992, settings: { slidesToShow: 1 } }]
      });
    }

    // Click speciality to filter doctors by department
    $('.specialities-slider').on('click', '.speicality-item', function(){
      var key = $(this).find('p').text().trim().toLowerCase();
      if (!$doc.length) return;
      $doc.slick('slickUnfilter');
      $doc.slick('slickFilter', function(){
        var dep = ($(this).find('.speciality').text() || '')
          .toString().trim().toLowerCase();
        return dep.indexOf(key) !== -1;
      });
      var obj = $doc.slick('getSlick');
      if (obj && obj.slideCount === 0) {
        $doc.slick('slickUnfilter');
      }
    });
  });
})(jQuery);

