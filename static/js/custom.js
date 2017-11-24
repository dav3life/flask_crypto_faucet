


jQuery(function($) {
 // "use strict";
/* ==============================================
   Countdown
=============================================== */
  // Create a countdown instance. Change the launchDay according to your needs.
  // The month ranges from 0 to 11. I specify the month from 1 to 12 and manually subtract the 1.
  // Thus the launchDay below denotes 7 May, 2014.
  var launchDay = new Date(06, 3-1, 2016);
  $('#timer').countdown({
  until: launchDay
  });


/* ==============================================
  Bx Slider
=============================================== */

  $('.bxslider').bxSlider({
      auto: true,
      pager:false,
      mode: 'fade',
      speed: 1500,
      pause:5000
      });

    /* ----------------------------------------------------------- */
   /*  Animation
   /* ----------------------------------------------------------- */
        new WOW().init();

   /* ==============================================
    Bactstretch js
=============================================== */
      $.backstretch([
          "static/images/bx-slider/bg2.jpg",
          "static/images/bx-slider/bg1.jpg",
          "static/images/bx-slider/bg3.jpg"
        ], {
            fade: 750,
            duration: 4000
        });   



});